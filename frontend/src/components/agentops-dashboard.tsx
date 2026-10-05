"use client";

import { FormEvent, useEffect, useMemo, useState } from "react";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

type TraceStep = {
  step_id: string;
  tool_name: string;
  rationale: string;
  permission: "read" | "write";
  status:
    | "pending"
    | "running"
    | "completed"
    | "awaiting_approval"
    | "failed";
  result: unknown;
  error: string | null;
};

type AgentRun = {
  run_id: string;
  workspace_id: string;
  request: string;
  status: "running" | "completed" | "awaiting_approval" | "failed";
  final_response: string | null;
  trace: TraceStep[];
};

type SearchHit = {
  source_id: string;
  source_name: string;
  chunk_id: string;
  score: number;
  text: string;
};

type EvalPayload = {
  passed: boolean;
  cases: number;
  retrieval_hit_rate_at_2?: number;
  tool_selection_accuracy?: number;
};

type SpeechRecognitionAlternativeLike = {
  transcript: string;
};

type SpeechRecognitionResultLike = {
  readonly [index: number]: SpeechRecognitionAlternativeLike;
  length: number;
};

type SpeechRecognitionEventLike = {
  results: ArrayLike<SpeechRecognitionResultLike>;
};

type SpeechRecognitionLike = {
  lang: string;
  interimResults: boolean;
  continuous: boolean;
  start: () => void;
  onstart: (() => void) | null;
  onresult: ((event: SpeechRecognitionEventLike) => void) | null;
  onerror: (() => void) | null;
  onend: (() => void) | null;
};

type SpeechRecognitionConstructorLike = new () => SpeechRecognitionLike;

function getSpeechRecognitionConstructor() {
  if (typeof window === "undefined") return undefined;

  const voiceWindow = window as typeof window & {
    SpeechRecognition?: SpeechRecognitionConstructorLike;
    webkitSpeechRecognition?: SpeechRecognitionConstructorLike;
  };

  return voiceWindow.SpeechRecognition ?? voiceWindow.webkitSpeechRecognition;
}

const quickPrompts = [
  "What is the refund window?",
  "Summarize renewal risk for Acme.",
  "Escalate Acme and create a support ticket.",
];

function StatusDot({ tone = "green" }: { tone?: "green" | "amber" | "blue" }) {
  const classes = {
    green: "bg-emerald-400",
    amber: "bg-amber-400",
    blue: "bg-sky-400",
  };
  return <span className={"inline-block h-2 w-2 rounded-full " + classes[tone]} />;
}

function prettyToolName(value: string) {
  return value
    .split("_")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

export default function AgentOpsDashboard() {
  const [health, setHealth] = useState<"loading" | "online" | "offline">("loading");
  const [ragEval, setRagEval] = useState<EvalPayload | null>(null);
  const [agentEval, setAgentEval] = useState<EvalPayload | null>(null);
  const [prompt, setPrompt] = useState(quickPrompts[1]);
  const [run, setRun] = useState<AgentRun | null>(null);
  const [running, setRunning] = useState(false);
  const [runError, setRunError] = useState("");
  const [searchQuery, setSearchQuery] = useState("express shipping");
  const [searchHits, setSearchHits] = useState<SearchHit[]>([]);
  const [searching, setSearching] = useState(false);
  const [sources, setSources] = useState<
    Array<{ source_id: string; source_name: string; chunks: number }>
  >([]);
  const [voiceSupported, setVoiceSupported] = useState(false);
  const [speechSupported, setSpeechSupported] = useState(false);
  const [listening, setListening] = useState(false);
  const [voiceError, setVoiceError] = useState("");

  const pendingApproval = useMemo(
    () => run?.trace.find((step) => step.status === "awaiting_approval"),
    [run],
  );

  useEffect(() => {
    const capabilityTimer = window.setTimeout(() => {
      setVoiceSupported(Boolean(getSpeechRecognitionConstructor()));
      setSpeechSupported(
        "speechSynthesis" in window && "SpeechSynthesisUtterance" in window,
      );
    }, 0);

    async function bootstrap() {
      try {
        const [healthResponse, ragResponse, agentResponse, sourceResponse] =
          await Promise.all([
            fetch(API_BASE + "/health"),
            fetch(API_BASE + "/api/v1/evaluation/rag"),
            fetch(API_BASE + "/api/v1/evaluation/agents"),
            fetch(API_BASE + "/api/v1/knowledge/demo-retail/sources"),
          ]);

        setHealth(healthResponse.ok ? "online" : "offline");

        if (ragResponse.ok) {
          setRagEval(await ragResponse.json());
        }

        if (agentResponse.ok) {
          setAgentEval(await agentResponse.json());
        }

        if (sourceResponse.ok) {
          setSources(await sourceResponse.json());
        }
      } catch {
        setHealth("offline");
      }
    }

    void bootstrap();

    return () => window.clearTimeout(capabilityTimer);
  }, []);

  function startVoiceCapture() {
    setVoiceError("");
    const Recognition = getSpeechRecognitionConstructor();

    if (!Recognition) {
      setVoiceSupported(false);
      setVoiceError("Speech recognition is not available in this browser.");
      return;
    }

    const recognition = new Recognition();
    recognition.lang = navigator.language || "en-IN";
    recognition.interimResults = false;
    recognition.continuous = false;
    recognition.onstart = () => setListening(true);
    recognition.onresult = (event) => {
      const transcript = event.results[0]?.[0]?.transcript?.trim();
      if (transcript) {
        setPrompt(transcript);
      } else {
        setVoiceError("No speech was detected. Try again.");
      }
    };
    recognition.onerror = () => {
      setVoiceError("Microphone input failed or permission was denied.");
      setListening(false);
    };
    recognition.onend = () => setListening(false);

    try {
      recognition.start();
    } catch {
      setVoiceError("Unable to start microphone input.");
      setListening(false);
    }
  }

  function speakLatestResponse() {
    if (!run?.final_response || !speechSupported) return;

    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(run.final_response);
    utterance.lang = navigator.language || "en-IN";
    utterance.rate = 0.98;
    window.speechSynthesis.speak(utterance);
  }

  async function executeAgent(value: string) {
    setRunning(true);
    setRunError("");

    try {
      const response = await fetch(API_BASE + "/api/v1/agents/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          workspace_id: "demo-retail",
          request: value,
        }),
      });

      if (!response.ok) {
        throw new Error("Agent request failed.");
      }

      setRun(await response.json());
    } catch (error) {
      setRunError(error instanceof Error ? error.message : "Agent request failed.");
    } finally {
      setRunning(false);
    }
  }

  async function handleAgentSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!prompt.trim()) return;
    await executeAgent(prompt.trim());
  }

  async function approvePendingStep() {
    if (!run || !pendingApproval) return;

    const response = await fetch(
      API_BASE +
        "/api/v1/agents/runs/" +
        run.run_id +
        "/approve/" +
        pendingApproval.step_id,
      { method: "POST" },
    );

    if (response.ok) {
      setRun(await response.json());
    }
  }

  async function handleKnowledgeSearch(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!searchQuery.trim()) return;

    setSearching(true);

    try {
      const response = await fetch(API_BASE + "/api/v1/knowledge/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          workspace_id: "demo-retail",
          query: searchQuery.trim(),
          top_k: 3,
        }),
      });

      if (response.ok) {
        const payload = await response.json();
        setSearchHits(payload.hits || []);
      }
    } finally {
      setSearching(false);
    }
  }

  const metricCards = [
    {
      label: "Knowledge sources",
      value: sources.length ? String(sources.length) : "3",
      detail: "Tenant-scoped indexed sources",
    },
    {
      label: "RAG hit-rate@2",
      value: ragEval ? Math.round((ragEval.retrieval_hit_rate_at_2 || 0) * 100) + "%" : "—",
      detail: ragEval?.passed ? "Evaluation passing" : "Loading evaluation",
    },
    {
      label: "Agent routing",
      value: agentEval ? Math.round((agentEval.tool_selection_accuracy || 0) * 100) + "%" : "—",
      detail: agentEval?.passed ? "Tool selection passing" : "Loading evaluation",
    },
    {
      label: "API status",
      value: health === "online" ? "Online" : health === "offline" ? "Offline" : "Checking",
      detail: "FastAPI backend",
    },
  ];

  return (
    <main className="min-h-screen bg-[var(--background)] text-[var(--foreground)]">
      <div className="mx-auto grid min-h-screen max-w-[1600px] grid-cols-1 lg:grid-cols-[250px_1fr]">
        <aside className="border-b border-white/10 bg-[#0c111b] px-5 py-6 lg:border-b-0 lg:border-r">
          <div className="mb-8 flex items-center gap-3 px-2">
            <div className="grid h-10 w-10 place-items-center rounded-xl bg-gradient-to-br from-cyan-400 to-indigo-500 font-black text-slate-950">
              A
            </div>
            <div>
              <p className="text-sm font-semibold tracking-wide text-white">AgentOps AI</p>
              <p className="text-xs text-slate-400">Operations intelligence</p>
            </div>
          </div>

          <nav className="grid gap-1 text-sm">
            {["Overview", "AI Copilot", "Knowledge Base", "Agent Runs", "Approvals", "Evaluation"].map(
              (item, index) => (
                <button
                  key={item}
                  className={
                    "rounded-lg px-3 py-2.5 text-left transition " +
                    (index === 0
                      ? "bg-white/10 font-medium text-white"
                      : "text-slate-400 hover:bg-white/5 hover:text-white")
                  }
                >
                  {item}
                </button>
              ),
            )}
          </nav>

          <div className="mt-10 rounded-xl border border-cyan-400/15 bg-cyan-400/5 p-4">
            <div className="mb-2 flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.16em] text-cyan-300">
              <StatusDot tone={health === "online" ? "green" : health === "offline" ? "amber" : "blue"} />
              {health === "online" ? "API online" : health === "offline" ? "API offline" : "Checking API"}
            </div>
            <p className="text-xs leading-5 text-slate-400">
              Synthetic demo data. Every write action requires explicit approval.
            </p>
          </div>
        </aside>

        <section className="min-w-0">
          <header className="flex flex-col gap-4 border-b border-white/10 bg-[#0e1522]/90 px-6 py-5 backdrop-blur md:flex-row md:items-center md:justify-between lg:px-10">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-cyan-300">Workspace</p>
              <h1 className="mt-1 text-2xl font-semibold text-white">Northstar Commerce</h1>
            </div>
            <div className="flex flex-wrap items-center gap-3">
              <span className="rounded-lg border border-white/10 bg-white/5 px-4 py-2 text-sm text-slate-300">
                Multi-agent demo
              </span>
              <button
                onClick={() => void executeAgent("Summarize renewal risk for Acme.")}
                className="rounded-lg bg-cyan-400 px-4 py-2 text-sm font-semibold text-slate-950 shadow-lg shadow-cyan-400/10"
              >
                Run demo agent
              </button>
            </div>
          </header>

          <div className="space-y-8 px-6 py-8 lg:px-10">
            <section className="grid gap-6 xl:grid-cols-[1.15fr_.85fr]">
              <article className="panel p-6 lg:p-7">
                <div className="mb-5">
                  <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-1 text-xs font-medium text-emerald-300">
                    <StatusDot tone="green" /> Approval-gated tool calling
                  </div>
                  <h2 className="text-2xl font-semibold text-white">AI Operations Copilot</h2>
                  <p className="mt-2 text-sm leading-6 text-slate-400">
                    Ask grounded questions or run tool-using business workflows. Write actions stop for human approval.
                  </p>
                </div>

                <div className="mb-4 flex flex-wrap gap-2">
                  {quickPrompts.map((item) => (
                    <button
                      key={item}
                      onClick={() => setPrompt(item)}
                      className="rounded-full border border-white/10 bg-white/5 px-3 py-1.5 text-xs text-slate-300 hover:border-cyan-300/30"
                    >
                      {item}
                    </button>
                  ))}
                </div>

                <form onSubmit={handleAgentSubmit} className="space-y-3">
                  <textarea
                    value={prompt}
                    onChange={(event) => setPrompt(event.target.value)}
                    rows={4}
                    className="w-full resize-none rounded-xl border border-white/10 bg-black/20 p-4 text-sm text-slate-200 outline-none transition focus:border-cyan-300/40"
                    placeholder="Ask AgentOps to research or take an approved action..."
                  />
                  <div className="flex flex-wrap items-center gap-2">
                    <button
                      type="button"
                      onClick={startVoiceCapture}
                      disabled={!voiceSupported || listening}
                      className="rounded-lg border border-white/10 bg-white/5 px-4 py-2.5 text-sm font-medium text-slate-200 disabled:cursor-not-allowed disabled:opacity-40"
                    >
                      {listening
                        ? "Listening..."
                        : voiceSupported
                          ? "Use microphone"
                          : "Voice unavailable"}
                    </button>
                    <button
                      type="submit"
                      disabled={running}
                      className="rounded-lg bg-cyan-400 px-4 py-2.5 text-sm font-semibold text-slate-950 disabled:opacity-50"
                    >
                      {running ? "Running agent..." : "Run agent"}
                    </button>
                  </div>
                  <p className="text-xs leading-5 text-slate-500">
                    Voice uses your browser&apos;s speech APIs and depends on browser microphone permissions.
                  </p>
                </form>

                {voiceError && <p className="mt-4 text-sm text-amber-300">{voiceError}</p>}
                {runError && <p className="mt-4 text-sm text-rose-300">{runError}</p>}

                {run && (
                  <div className="mt-6 rounded-xl border border-white/10 bg-black/20 p-4">
                    <div className="flex flex-wrap items-center justify-between gap-3">
                      <div>
                        <p className="text-xs uppercase tracking-[0.16em] text-slate-500">Run {run.run_id}</p>
                        <p className="mt-1 text-sm font-medium text-slate-200">{run.final_response || "Processing..."}</p>
                      </div>
                      <span
                        className={
                          "rounded-full px-2.5 py-1 text-xs font-medium " +
                          (run.status === "completed"
                            ? "bg-emerald-400/10 text-emerald-300"
                            : run.status === "awaiting_approval"
                              ? "bg-amber-400/10 text-amber-300"
                              : "bg-sky-400/10 text-sky-300")
                        }
                      >
                        {run.status.replace("_", " ")}
                      </span>
                    </div>

                    {run.final_response && (
                      <button
                        type="button"
                        onClick={speakLatestResponse}
                        disabled={!speechSupported}
                        className="mt-4 rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-xs font-medium text-slate-200 disabled:cursor-not-allowed disabled:opacity-40"
                      >
                        {speechSupported ? "Speak response" : "Speech output unavailable"}
                      </button>
                    )}

                    {pendingApproval && (
                      <div className="mt-4 flex items-center justify-between gap-3 rounded-lg border border-amber-400/20 bg-amber-400/5 p-3">
                        <div>
                          <p className="text-sm font-medium text-amber-200">Approval required</p>
                          <p className="mt-1 text-xs text-amber-100/60">
                            {prettyToolName(pendingApproval.tool_name)} is a write action.
                          </p>
                        </div>
                        <button
                          onClick={() => void approvePendingStep()}
                          className="rounded-md bg-amber-300 px-3 py-2 text-xs font-semibold text-slate-950"
                        >
                          Approve action
                        </button>
                      </div>
                    )}

                    <div className="mt-5 space-y-3">
                      {run.trace.map((step, index) => (
                        <div key={step.step_id} className="flex gap-3">
                          <div className="grid h-7 w-7 shrink-0 place-items-center rounded-full border border-white/10 bg-white/5 text-xs text-slate-300">
                            {index + 1}
                          </div>
                          <div className="min-w-0 flex-1">
                            <div className="flex flex-wrap items-center gap-2">
                              <p className="text-sm font-medium text-slate-200">{prettyToolName(step.tool_name)}</p>
                              <span className="text-[11px] uppercase tracking-wide text-slate-500">{step.permission}</span>
                              <span className="text-xs text-cyan-300">{step.status.replace("_", " ")}</span>
                            </div>
                            <p className="mt-1 text-xs leading-5 text-slate-500">{step.rationale}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </article>

              <article className="panel p-6 lg:p-7">
                <div>
                  <h2 className="text-xl font-semibold text-white">Knowledge search</h2>
                  <p className="mt-2 text-sm text-slate-400">Inspect the same tenant-scoped retrieval layer used by agents.</p>
                </div>

                <form onSubmit={handleKnowledgeSearch} className="mt-5 flex gap-2">
                  <input
                    value={searchQuery}
                    onChange={(event) => setSearchQuery(event.target.value)}
                    className="min-w-0 flex-1 rounded-lg border border-white/10 bg-black/20 px-3 py-2.5 text-sm text-slate-200 outline-none focus:border-cyan-300/40"
                    placeholder="Search workspace knowledge"
                  />
                  <button className="rounded-lg border border-white/10 bg-white/5 px-3 py-2.5 text-sm text-slate-200">
                    {searching ? "..." : "Search"}
                  </button>
                </form>

                <div className="mt-5 space-y-3">
                  {searchHits.length === 0 && (
                    <p className="rounded-lg border border-dashed border-white/10 p-4 text-sm text-slate-500">
                      Run a search to inspect retrieved evidence and similarity scores.
                    </p>
                  )}
                  {searchHits.map((hit) => (
                    <div key={hit.chunk_id} className="rounded-xl border border-white/10 bg-white/[0.025] p-4">
                      <div className="flex items-center justify-between gap-3">
                        <p className="text-sm font-medium text-slate-200">{hit.source_name}</p>
                        <span className="text-xs text-cyan-300">{hit.score.toFixed(3)}</span>
                      </div>
                      <p className="mt-2 line-clamp-3 text-xs leading-5 text-slate-500">{hit.text}</p>
                    </div>
                  ))}
                </div>
              </article>
            </section>

            <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
              {metricCards.map((card) => (
                <article key={card.label} className="panel p-5">
                  <p className="text-sm text-slate-400">{card.label}</p>
                  <p className="mt-3 text-3xl font-semibold tracking-tight text-white">{card.value}</p>
                  <p className="mt-2 text-xs text-slate-500">{card.detail}</p>
                </article>
              ))}
            </section>

            <section className="panel overflow-hidden">
              <div className="flex flex-col gap-3 border-b border-white/10 px-5 py-4 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <h3 className="font-semibold text-white">Indexed knowledge sources</h3>
                  <p className="mt-1 text-xs text-slate-500">Loaded directly from the FastAPI RAG service</p>
                </div>
                <span className="rounded-full bg-cyan-400/10 px-2.5 py-1 text-xs text-cyan-300">
                  {sources.length} sources
                </span>
              </div>
              <div className="grid gap-px bg-white/5 md:grid-cols-3">
                {sources.map((source) => (
                  <div key={source.source_id} className="bg-[#111a29] p-5">
                    <div className="mb-4 flex items-center gap-2 text-xs text-emerald-300">
                      <StatusDot tone="green" /> Ready
                    </div>
                    <p className="text-sm font-medium text-slate-200">{source.source_name}</p>
                    <p className="mt-2 text-xs text-slate-500">{source.chunks} indexed chunk(s)</p>
                  </div>
                ))}
              </div>
            </section>
          </div>
        </section>
      </div>
    </main>
  );
}
