import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "AgentOps AI — Multi-Agent RAG SaaS",
  description:
    "Production-style AI operations workspace with RAG, agents, tool calling, approvals, evaluation, and observability.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className={geistSans.variable + " " + geistMono.variable + " h-full antialiased"}>
      <body className="min-h-full">{children}</body>
    </html>
  );
}
