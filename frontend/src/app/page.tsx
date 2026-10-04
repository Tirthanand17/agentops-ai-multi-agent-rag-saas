const metricCards = [
  { label: "Knowledge sources", value: "24", detail: "18 indexed · 6 queued" },
  { label: "Agent success rate", value: "94.2%", detail: "+3.8% this week" },
  { label: "Median latency", value: "1.7s", detail: "P95 3.9s" },
  { label: "Approval queue", value: "3", detail: "2 write actions · 1 webhook" },
];

const agentRuns = [
  { task: "Summarize renewal risk for Acme", agent: "Account Copilot", status: "Completed", tools: "Knowledge → CRM → KPI", time: "41s ago" },
  { task: "Create support escalation draft", agent: "Support Agent", status: "Awaiting approval", tools: "Knowledge → Ticket", time: "2m ago" },
  { task: "Find Q3 return-policy conflicts", agent: "Research Agent", status: "Completed", tools: "Vector Search → Rerank", time: "7m ago" },
];

const knowledgeSources = [
  { name: "Customer Success Playbook", type: "PDF", chunks: 42, health: "Ready" },
  { name: "Q3 Pricing & Packaging", type: "DOCX", chunks: 28, health: "Ready" },
  { name: "Support Policies", type: "PDF", chunks: 36, health: "Ready" },
  { name: "Northstar CRM Export", type: "CSV", chunks: 14, health: "Syncing" },
];

function StatusDot({ tone = "green" }: { tone?: "green" | "amber" | "blue" }) {
  const classes = {
    green: "bg-emerald-400",
    amber: "bg-amber-400",
    blue: "bg-sky-400",
  };
  return <span className={"inline-block h-2 w-2 rounded-full " + classes[tone]} />;
}

export default function Home() {
  return (
    <main className="min-h-screen bg-[var(--background)] text-[var(--foreground)]">
      <div className="mx-auto grid min-h-screen max-w-[1600px] grid-cols-1 lg:grid-cols-[250px_1fr]">
        <aside className="border-b border-white/10 bg-[#0c111b] px-5 py-6 lg:border-b-0 lg:border-r">
          <div className="mb-8 flex items-center gap-3 px-2">
            <div className="grid h-10 w-10 place-items-center rounded-xl bg-gradient-to-br from-cyan-400 to-indigo-500 font-black text-slate-950">A</div>
            <div>
              <p className="text-sm font-semibold tracking-wide text-white">AgentOps AI</p>
              <p className="text-xs text-slate-400">Operations intelligence</p>
            </div>
          </div>

          <nav className="grid gap-1 text-sm">
            {["Overview", "AI Copilot", "Knowledge Base", "Agent Runs", "Approvals", "Evaluation"].map((item, index) => (
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
            ))}
          </nav>

          <div className="mt-10 rounded-xl border border-cyan-400/15 bg-cyan-400/5 p-4">
            <div className="mb-2 flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.16em] text-cyan-300">
              <StatusDot tone="green" /> System online
            </div>
            <p className="text-xs leading-5 text-slate-400">
              Demo workspace uses synthetic data and approval gates for every write action.
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
              <button className="rounded-lg border border-white/10 bg-white/5 px-4 py-2 text-sm text-slate-200">View traces</button>
              <button className="rounded-lg bg-cyan-400 px-4 py-2 text-sm font-semibold text-slate-950 shadow-lg shadow-cyan-400/10">New agent run</button>
            </div>
          </header>

          <div className="space-y-8 px-6 py-8 lg:px-10">
            <section className="overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-[#131d30] via-[#101827] to-[#0f1724] p-6 shadow-2xl shadow-black/10 lg:p-8">
              <div className="grid gap-8 xl:grid-cols-[1.25fr_.75fr]">
                <div>
                  <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-1 text-xs font-medium text-emerald-300">
                    <StatusDot tone="green" /> Grounded answers enabled
                  </div>
                  <h2 className="max-w-3xl text-3xl font-semibold tracking-tight text-white lg:text-4xl">
                    One workspace for knowledge, agents, approvals, and AI quality.
                  </h2>
                  <p className="mt-4 max-w-2xl text-sm leading-7 text-slate-400 lg:text-base">
                    AgentOps combines cited RAG, tool-using agents, human approval gates, and execution traces so teams can automate real work without losing visibility or control.
                  </p>
                  <div className="mt-6 flex flex-wrap gap-3">
                    <span className="chip">RAG + citations</span>
                    <span className="chip">Tool calling</span>
                    <span className="chip">MCP-style tools</span>
                    <span className="chip">Human approval</span>
                    <span className="chip">Evaluation</span>
                  </div>
                </div>

                <div className="rounded-2xl border border-white/10 bg-black/20 p-5">
                  <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">Latest agent trace</p>
                  <div className="mt-5 space-y-4">
                    {[
                      ["1", "Retrieve", "4 cited chunks"],
                      ["2", "Plan", "3 tool steps"],
                      ["3", "CRM lookup", "Customer found"],
                      ["4", "KPI calculator", "Risk score 0.71"],
                    ].map(([step, title, detail], index) => (
                      <div key={step} className="flex gap-3">
                        <div className="relative flex flex-col items-center">
                          <div className="grid h-7 w-7 place-items-center rounded-full border border-cyan-300/20 bg-cyan-300/10 text-xs font-semibold text-cyan-200">{step}</div>
                          {index < 3 && <div className="mt-1 h-6 w-px bg-white/10" />}
                        </div>
                        <div className="pt-1">
                          <p className="text-sm font-medium text-slate-200">{title}</p>
                          <p className="mt-0.5 text-xs text-slate-500">{detail}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
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

            <section className="grid gap-6 xl:grid-cols-[1.35fr_.65fr]">
              <article className="panel overflow-hidden">
                <div className="flex items-center justify-between border-b border-white/10 px-5 py-4">
                  <div>
                    <h3 className="font-semibold text-white">Recent agent runs</h3>
                    <p className="mt-1 text-xs text-slate-500">Plans, tools, and execution state</p>
                  </div>
                  <span className="text-xs text-cyan-300">Live trace</span>
                </div>
                <div className="divide-y divide-white/5">
                  {agentRuns.map((run) => (
                    <div key={run.task} className="grid gap-3 px-5 py-4 md:grid-cols-[1.25fr_.8fr_.8fr_auto] md:items-center">
                      <div>
                        <p className="text-sm font-medium text-slate-200">{run.task}</p>
                        <p className="mt-1 text-xs text-slate-500">{run.agent}</p>
                      </div>
                      <p className="text-xs text-slate-400">{run.tools}</p>
                      <div className="flex items-center gap-2 text-xs text-slate-300">
                        <StatusDot tone={run.status === "Completed" ? "green" : "amber"} />
                        {run.status}
                      </div>
                      <p className="text-xs text-slate-500">{run.time}</p>
                    </div>
                  ))}
                </div>
              </article>

              <article className="panel p-5">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-semibold text-white">Approval queue</h3>
                    <p className="mt-1 text-xs text-slate-500">Human-in-the-loop safety</p>
                  </div>
                  <span className="rounded-full bg-amber-400/10 px-2.5 py-1 text-xs font-medium text-amber-300">3 pending</span>
                </div>
                <div className="mt-5 space-y-3">
                  {[
                    ["Create escalation ticket", "Support Agent"],
                    ["Send retention email", "Account Copilot"],
                    ["POST partner webhook", "Workflow Agent"],
                  ].map(([task, agent]) => (
                    <div key={task} className="rounded-xl border border-white/10 bg-white/[0.025] p-4">
                      <p className="text-sm font-medium text-slate-200">{task}</p>
                      <p className="mt-1 text-xs text-slate-500">{agent}</p>
                      <div className="mt-3 flex gap-2">
                        <button className="rounded-md bg-emerald-400/10 px-3 py-1.5 text-xs font-medium text-emerald-300">Approve</button>
                        <button className="rounded-md bg-white/5 px-3 py-1.5 text-xs text-slate-400">Review</button>
                      </div>
                    </div>
                  ))}
                </div>
              </article>
            </section>

            <section className="panel overflow-hidden">
              <div className="flex flex-col gap-3 border-b border-white/10 px-5 py-4 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <h3 className="font-semibold text-white">Knowledge base</h3>
                  <p className="mt-1 text-xs text-slate-500">Tenant-scoped sources with retrieval health</p>
                </div>
                <button className="self-start rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-xs text-slate-300 sm:self-auto">Add source</button>
              </div>
              <div className="grid gap-px bg-white/5 md:grid-cols-2 xl:grid-cols-4">
                {knowledgeSources.map((source) => (
                  <div key={source.name} className="bg-[#111a29] p-5">
                    <div className="mb-5 flex items-center justify-between">
                      <span className="rounded-md border border-white/10 bg-white/5 px-2 py-1 text-[11px] font-semibold text-slate-400">{source.type}</span>
                      <span className="flex items-center gap-2 text-xs text-slate-400">
                        <StatusDot tone={source.health === "Ready" ? "green" : "blue"} />
                        {source.health}
                      </span>
                    </div>
                    <p className="text-sm font-medium text-slate-200">{source.name}</p>
                    <p className="mt-2 text-xs text-slate-500">{source.chunks} indexed chunks</p>
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
