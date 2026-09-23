"use client";

import React, { useState } from "react";
import Image from "next/image";
import {
  Activity,
  CheckCircle2,
  Cpu,
  Database,
  ExternalLink,
  Layers,
  Maximize2,
  Search,
  Shield,
  X,
  Zap,
  Grid,
} from "lucide-react";

interface DiagramSpec {
  id: "pipeline" | "cloud" | "rag";
  blueprintNumber: string;
  title: string;
  badge: string;
  imageSrc: string;
  headline: string;
  description: string;
  annotations: {
    label: string;
    note: string;
    detail: string;
    direction: "ann-n";
    color: "ann-amber" | "ann-blue" | "ann-green" | "ann-purple" | "ann-red";
  }[];
  specifications: {
    category: string;
    items: { label: string; value: string }[];
  }[];
}

const DIAGRAMS: DiagramSpec[] = [
  {
    id: "pipeline",
    blueprintNumber: "BLUEPRINT 01",
    title: "Detection & Case Triage Pipeline",
    badge: "Real-Time Surveillance",
    imageSrc: "/architecture/pipeline-architecture.png",
    headline: "End-to-End Real-Time Transaction Intelligence Flow",
    description:
      "Captures transactions from multi-channel sources, extracts 17 behavioral dimensions in <5ms, evaluates risk across XGBoost, Isolation Forest, and deterministic rules, explains drivers via TreeSHAP, and delivers case dossiers to human analysts.",
    annotations: [
      {
        label: "17-Dim Feature Pipeline",
        note: "< 5ms latency",
        detail: "Extracts velocity, geo-corridor, and device fingerprint hashes",
        direction: "ann-n",
        color: "ann-amber",
      },
      {
        label: "Hybrid AI Scoring",
        note: "XGBoost + iForest",
        detail: "Calibrated weighted ensemble (0.45 XGB + 0.25 iF + 0.30 Rules)",
        direction: "ann-n",
        color: "ann-purple",
      },
      {
        label: "TreeSHAP Attribution",
        note: "top 5 risk drivers",
        detail: "Mathematical feature Shapley attribution per transaction",
        direction: "ann-n",
        color: "ann-blue",
      },
      {
        label: "Human Case Triage",
        note: "analyst sign-off",
        detail: "Clear, escalate, or confirm with sealed audit ledger",
        direction: "ann-n",
        color: "ann-green",
      },
    ],
    specifications: [
      {
        category: "Ingestion & Scoring",
        items: [
          { label: "End-to-End Latency", value: "< 15 ms" },
          { label: "Feature Extraction", value: "17 Dimensions" },
          { label: "Scoring Range", value: "0–100 Calibrated" },
        ],
      },
      {
        category: "Machine Learning",
        items: [
          { label: "Supervised Engine", value: "XGBoost v1.0.0 (ROC-AUC 0.9999)" },
          { label: "Anomaly Engine", value: "Isolation Forest (Delta +0.5472)" },
          { label: "Local Attribution", value: "TreeSHAP Shapley Values" },
        ],
      },
      {
        category: "Triage & Persistence",
        items: [
          { label: "Alert Trigger", value: "Score >= 60.0" },
          { label: "Audit Ledger", value: "Neon PostgreSQL 18.6" },
          { label: "Decision SLA", value: "Human-in-the-Loop Sign-off" },
        ],
      },
    ],
  },
  {
    id: "cloud",
    blueprintNumber: "BLUEPRINT 02",
    title: "Enterprise Cloud & Microservices Topology",
    badge: "Cloud Architecture",
    imageSrc: "/architecture/cloud-infrastructure.png",
    headline: "Decoupled Dual-Microservice Infrastructure",
    description:
      "Production-hardened deployment architecture separating Next.js 15 frontend client, FastAPI Core Backend (port 8000), and FastAPI ML Inference Microservice (port 8001) connected to Neon PostgreSQL and Supabase Cloud Storage.",
    annotations: [
      {
        label: "FastAPI Core (Port 8000)",
        note: "orchestration API",
        detail: "Handles transaction ingestion, case management, and audit records",
        direction: "ann-n",
        color: "ann-blue",
      },
      {
        label: "ML Engine (Port 8001)",
        note: "real-time inference",
        detail: "FastAPI microservice executing TreeSHAP and ensemble scoring",
        direction: "ann-n",
        color: "ann-purple",
      },
      {
        label: "Neon PostgreSQL 18.6",
        note: "pgvector enabled",
        detail: "Serverless Postgres with 17 operational tables and vector index",
        direction: "ann-n",
        color: "ann-green",
      },
      {
        label: "Automated Retraining",
        note: "every 12 hours",
        detail: "APScheduler background worker with zero-downtime model swap",
        direction: "ann-n",
        color: "ann-amber",
      },
    ],
    specifications: [
      {
        category: "Microservices",
        items: [
          { label: "Core Backend API", value: "FastAPI / Python 3.12 (Port 8000)" },
          { label: "ML Inference Engine", value: "FastAPI / Uvicorn (Port 8001)" },
          { label: "Frontend Web Client", value: "Next.js 15 App Router (Port 3000)" },
        ],
      },
      {
        category: "Persistence & Cloud",
        items: [
          { label: "Primary Database", value: "Neon PostgreSQL 18.6 (AWS us-east-2)" },
          { label: "Object Storage", value: "Supabase (3 buckets)" },
          { label: "Authentication", value: "Clerk JWT + Route Middleware" },
        ],
      },
      {
        category: "MLOps & Reliability",
        items: [
          { label: "Retraining Interval", value: "Every 12 Hours Automated" },
          { label: "Model Hot-Reload", value: "Zero-Downtime Memory Swap" },
          { label: "Connection Pooling", value: "Asyncpg + PgBouncer" },
        ],
      },
    ],
  },
  {
    id: "rag",
    blueprintNumber: "BLUEPRINT 03",
    title: "Grounded Vector RAG & Compliance Flow",
    badge: "Copilot Intelligence",
    imageSrc: "/architecture/rag-workflow.png",
    headline: "Grounded Compliance RAG & Vector Retrieval Flow",
    description:
      "Regulatory investigation copilot connecting analyst queries to approved compliance SOPs (SOP-104, POL-201, REG-04) using 384-dimensional dense embeddings and pgvector cosine similarity matching without hallucination.",
    annotations: [
      {
        label: "Compliance Knowledge Base",
        note: "11 approved SOPs",
        detail: "Official institutional directives covering wire fraud and sanctions",
        direction: "ann-n",
        color: "ann-purple",
      },
      {
        label: "pgvector Index",
        note: "cosine similarity",
        detail: "Dense 384-dim semantic embeddings with cosine distance search",
        direction: "ann-n",
        color: "ann-green",
      },
      {
        label: "LLM Case Copilot",
        note: "strictly grounded",
        detail: "Reasoning bound to retrieved case evidence and SOP citations",
        direction: "ann-n",
        color: "ann-amber",
      },
      {
        label: "Zero-Hallucination Audit",
        note: "sealed audit trail",
        detail: "Verifiable section references logged with analyst decision sign-off",
        direction: "ann-n",
        color: "ann-blue",
      },
    ],
    specifications: [
      {
        category: "Vector Indexing",
        items: [
          { label: "Embedding Dimensions", value: "384 Dense Normalized" },
          { label: "Similarity Metric", value: "Cosine Similarity (<=>)" },
          { label: "Indexed Chunks", value: "14 Regulatory Vectors" },
        ],
      },
      {
        category: "Compliance Library",
        items: [
          { label: "Wire Protocol", value: "SOP-104 Rapid Wire Verification" },
          { label: "Sanctions Directive", value: "REG-04 / OFAC Sanctions" },
          { label: "Precedent Dossiers", value: "Executive BEC & CNP Protocols" },
        ],
      },
      {
        category: "Copilot Guardrails",
        items: [
          { label: "Strict Grounding", value: "Dossier & Policy Bound Only" },
          { label: "Source Attribution", value: "Document, Section & Relevance %" },
          { label: "Analyst Sign-off", value: "Clear / Escalate / Confirm Action" },
        ],
      },
    ],
  },
];

export function ArchitectureShowcase() {
  const [viewMode, setViewMode] = useState<"all" | "pipeline" | "cloud" | "rag">("all");
  const [activeModalImage, setActiveModalImage] = useState<DiagramSpec | null>(null);

  const displayedDiagrams =
    viewMode === "all" ? DIAGRAMS : DIAGRAMS.filter((d) => d.id === viewMode);

  return (
    <section id="architecture" className="py-20 px-4 sm:px-6 lg:px-8 max-w-6xl mx-auto border-t border-slate-200/70">
      {/* Section Header */}
      <div className="max-w-3xl mb-10">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-100 border border-slate-200 text-xs font-mono text-slate-700 mb-3">
          <Layers className="w-3.5 h-3.5 text-blue-600" />
          <span>Full Architectural Suite</span>
        </div>
        <h2 className="text-3xl sm:text-4xl font-semibold text-slate-900 tracking-tight">
          Visualized Engineering Topologies &amp; Workflows
        </h2>
        <p className="text-sm sm:text-base text-slate-600 leading-relaxed mt-3">
          Explore all three system architecture blueprints powering FinGuard AI: real-time detection pipelines, decoupled dual-microservices cloud infrastructure, and grounded compliance vector RAG workflows.
        </p>
      </div>

      {/* View Switcher Bar */}
      <div className="flex flex-wrap items-center gap-2 mb-10 p-1.5 bg-slate-100/90 rounded-2xl border border-slate-200/80 w-fit">
        <button
          type="button"
          onClick={() => setViewMode("all")}
          className={`inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-medium transition-all ${
            viewMode === "all"
              ? "bg-white text-slate-900 shadow-xs border border-slate-200 font-semibold"
              : "text-slate-600 hover:text-slate-900 hover:bg-white/50"
          }`}
        >
          <Grid className="w-3.5 h-3.5 text-blue-600" />
          <span>All 3 Architecture Blueprints</span>
        </button>

        {DIAGRAMS.map((diagram) => {
          const isActive = viewMode === diagram.id;
          return (
            <button
              key={diagram.id}
              type="button"
              onClick={() => setViewMode(diagram.id)}
              className={`px-3.5 py-2 rounded-xl text-xs font-medium transition-all ${
                isActive
                  ? "bg-white text-slate-900 shadow-xs border border-slate-200 font-semibold"
                  : "text-slate-600 hover:text-slate-900 hover:bg-white/50"
              }`}
            >
              {diagram.blueprintNumber}: {diagram.title}
            </button>
          );
        })}
      </div>

      {/* Diagram Blueprints List */}
      <div className="space-y-16">
        {displayedDiagrams.map((diagram) => (
          <article
            key={diagram.id}
            id={`diagram-${diagram.id}`}
            className="rounded-3xl border border-slate-200/90 bg-white shadow-sm overflow-hidden"
          >
            {/* Header & Badges */}
            <div className="p-6 sm:p-8 border-b border-slate-200/80 bg-slate-50/50">
              <div className="flex flex-wrap items-center justify-between gap-3 mb-2">
                <div className="inline-flex items-center gap-2">
                  <span className="text-xs font-mono font-bold tracking-wider text-blue-700 bg-blue-50 border border-blue-200 px-2.5 py-0.5 rounded-md">
                    {diagram.blueprintNumber}
                  </span>
                  <span className="text-xs font-mono text-slate-500 bg-slate-200/70 px-2 py-0.5 rounded-md">
                    {diagram.badge}
                  </span>
                </div>

                <button
                  type="button"
                  onClick={() => setActiveModalImage(diagram)}
                  className="inline-flex items-center gap-1.5 text-xs text-slate-700 hover:text-slate-900 px-3 py-1.5 rounded-lg bg-white hover:bg-slate-100 transition-colors border border-slate-200 shadow-2xs font-medium"
                >
                  <Maximize2 className="w-3.5 h-3.5 text-blue-600" />
                  <span>Inspect 4K Full Resolution</span>
                </button>
              </div>

              <h3 className="text-xl sm:text-2xl font-semibold text-slate-900 tracking-tight mt-2">
                {diagram.headline}
              </h3>
              <p className="text-xs sm:text-sm text-slate-600 leading-relaxed mt-2 max-w-3xl">
                {diagram.description}
              </p>
            </div>

            {/* Architecture Canvas in Terminal Frame */}
            <div className="bg-[#0B0F17] p-4 sm:p-6 lg:p-8">
              <div
                className="relative w-full aspect-[16/9] min-h-[380px] sm:min-h-[480px] lg:min-h-[560px] bg-[#0d1117] rounded-2xl border border-slate-800 shadow-2xl flex items-center justify-center p-3 sm:p-6 cursor-zoom-in group overflow-hidden"
                onClick={() => setActiveModalImage(diagram)}
              >
                <Image
                  src={diagram.imageSrc}
                  alt={diagram.title}
                  fill
                  sizes="(max-width: 1200px) 100vw, 1152px"
                  priority
                  className="object-contain p-2 sm:p-4 group-hover:scale-[1.01] transition-transform duration-300"
                />

                <div className="absolute bottom-4 right-4 bg-slate-900/90 backdrop-blur-sm border border-slate-700/80 text-slate-300 px-3 py-1.5 rounded-lg text-xs font-mono flex items-center gap-1.5 opacity-80 group-hover:opacity-100 transition-opacity">
                  <Search className="w-3.5 h-3.5 text-blue-400" />
                  <span>Click to zoom in 4K</span>
                </div>
              </div>
            </div>

            {/* Dedicated Non-Overlapping Neat-Annotations Callout Deck */}
            <div className="p-6 sm:p-8 bg-slate-50/70 border-t border-slate-200/80">
              <div className="flex items-center gap-2 mb-6">
                <span className="w-2 h-2 rounded-full bg-blue-600" />
                <span className="text-xs font-mono font-semibold uppercase tracking-wider text-slate-700">
                  Architectural Engineering Notes &amp; Highlights
                </span>
              </div>

              {/* 4-column isolated card grid: guarantees zero horizontal and zero vertical overlap */}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                {diagram.annotations.map((ann, idx) => (
                  <div
                    key={idx}
                    className="p-5 rounded-2xl bg-white border border-slate-200/90 shadow-2xs flex flex-col items-center justify-start text-center relative overflow-visible min-h-[145px] pb-16 transition-all hover:border-slate-300"
                  >
                    <span className="text-[10px] font-mono uppercase tracking-wider text-slate-400 mb-2">
                      Stage 0{idx + 1}
                    </span>

                    {/* Centered target badge with neat-annotations hand-drawn arrow pointing up from note */}
                    <div className="my-1 relative inline-block overflow-visible">
                      <span
                        className={`ann ${ann.direction} ${ann.color} font-semibold text-slate-900 text-xs px-2.5 py-1 rounded bg-slate-100/90 border border-slate-200/90 shadow-2xs`}
                        data-note={ann.note}
                      >
                        {ann.label}
                      </span>
                    </div>

                    {/* Subtitle with guaranteed mt-14 to sit cleanly below the handwritten cursive note */}
                    <p className="text-[11px] text-slate-500 mt-14 leading-relaxed max-w-[210px]">
                      {ann.detail}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            {/* Technical Specification Matrix */}
            <div className="bg-slate-900 p-6 sm:p-8 border-t border-slate-800 text-white">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs">
                {diagram.specifications.map((spec, i) => (
                  <div
                    key={i}
                    className="p-4 rounded-xl bg-slate-950/70 border border-slate-800/80 space-y-2.5"
                  >
                    <div className="font-semibold text-slate-300 text-xs uppercase tracking-wider font-mono">
                      {spec.category}
                    </div>
                    <div className="space-y-1.5">
                      {spec.items.map((item, j) => (
                        <div
                          key={j}
                          className="flex items-center justify-between text-[11px]"
                        >
                          <span className="text-slate-400">{item.label}</span>
                          <span className="text-slate-200 font-mono font-medium">
                            {item.value}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </article>
        ))}
      </div>

      {/* Fullscreen Lightbox Modal for 4K Inspection */}
      {activeModalImage && (
        <div className="fixed inset-0 z-50 bg-black/95 backdrop-blur-md flex flex-col p-4 sm:p-8 overflow-auto animate-in fade-in duration-200">
          <div className="flex items-center justify-between pb-4 max-w-7xl mx-auto w-full border-b border-slate-800 text-white">
            <div className="flex items-center gap-3">
              <span className="text-xs font-mono font-bold text-blue-400 bg-blue-950 border border-blue-800 px-2 py-0.5 rounded">
                {activeModalImage.blueprintNumber}
              </span>
              <span className="text-sm font-semibold tracking-tight">
                {activeModalImage.title}
              </span>
              <span className="text-xs text-slate-400 font-mono hidden sm:inline">
                4K Full-Resolution Blueprint
              </span>
            </div>
            <button
              type="button"
              onClick={() => setActiveModalImage(null)}
              className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          <div className="flex-1 flex items-center justify-center p-4 max-w-7xl mx-auto w-full relative min-h-[600px]">
            <Image
              src={activeModalImage.imageSrc}
              alt={activeModalImage.title}
              width={1920}
              height={1080}
              className="object-contain max-h-[85vh] w-auto rounded-lg shadow-2xl border border-slate-800"
            />
          </div>
        </div>
      )}
    </section>
  );
}
