import React from "react";
import Link from "next/link";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { RiskBadge } from "@/components/RiskBadge";
import { ArchitectureShowcase } from "@/components/ArchitectureShowcase";
import {
  ArrowRight,
  Shield,
  Activity,
  Layers,
  SearchCheck,
  CheckCircle2,
  FileText,
  Lock,
  Sparkles,
  Cpu,
  Fingerprint,
  ChevronRight,
  SlidersHorizontal,
  Clock,
  ExternalLink,
} from "lucide-react";

export default function LandingPage() {
  return (
    <div className="min-h-screen flex flex-col bg-[#fbfaf8] text-slate-900 selection:bg-blue-100 selection:text-blue-900 relative overflow-hidden">
      {/* Clean Subtle Background Grid */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-7xl h-[650px] pointer-events-none overflow-hidden opacity-40">
        <div className="absolute inset-0 bg-[radial-gradient(#cbd5e1_1px,transparent_1px)] [background-size:24px_24px] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)] opacity-60" />
      </div>

      <Navbar />

      <main className="flex-1 z-10">
        {/* Hero Section */}
        <section className="pt-16 sm:pt-20 pb-16 px-4 sm:px-6 lg:px-8 max-w-6xl mx-auto text-center">
          {/* Eyebrow Floating Pill */}
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white border border-slate-200 shadow-xs text-xs text-slate-700 mb-8 hover:border-slate-300 transition-colors">
            <span className="font-semibold text-slate-900">Dual-Engine ML Surveillance</span>
            <span className="text-slate-300">|</span>
            <span className="text-slate-600 font-mono">Grounded TreeSHAP</span>
          </div>

          {/* Hero Headline */}
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-semibold tracking-tight text-slate-900 leading-[1.12] max-w-4xl mx-auto mb-6">
            Explainable AI for financial fraud and{" "}
            <span className="text-slate-900">
              anomaly intelligence.
            </span>
          </h1>

          {/* Hero Subtitle */}
          <p className="text-base sm:text-lg text-slate-600 leading-relaxed max-w-2xl mx-auto mb-10 font-normal">
            FinGuard AI unifies supervised XGBoost classification, unsupervised anomaly scoring, and deterministic rule checks with mathematically grounded TreeSHAP attribution. Built for rapid investigation and accountable human sign-off.
          </p>

          {/* Primary Action Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-3.5 max-w-md mx-auto mb-12">
            <Link
              href="/demo"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3 rounded-full bg-slate-900 text-white font-semibold text-sm hover:bg-slate-800 transition-all shadow-md shadow-slate-900/20 hover:scale-[1.02] active:scale-[0.98]"
            >
              <Sparkles className="w-4 h-4 text-white/90" />
              <span>Explore Interactive Demo</span>
              <ArrowRight className="w-4 h-4 opacity-80" />
            </Link>

            <Link
              href="/dashboard"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3 rounded-full bg-white/90 border border-slate-200 text-slate-800 font-semibold text-sm hover:bg-slate-50 transition-all shadow-sm hover:scale-[1.02] active:scale-[0.98]"
            >
              <span>Access Risk Console</span>
            </Link>
          </div>

          {/* Key Assurance Indicators */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 max-w-3xl mx-auto pt-6 border-t border-slate-200/60 text-xs text-slate-500 font-medium">
            <div className="flex items-center justify-center gap-1.5">
              <CheckCircle2 className="w-3.5 h-3.5 text-slate-700" />
              <span>Three-Layer Triad</span>
            </div>
            <div className="flex items-center justify-center gap-1.5">
              <CheckCircle2 className="w-3.5 h-3.5 text-slate-700" />
              <span>TreeSHAP Attribution</span>
            </div>
            <div className="flex items-center justify-center gap-1.5">
              <CheckCircle2 className="w-3.5 h-3.5 text-slate-700" />
              <span>Grounded Policy RAG</span>
            </div>
            <div className="flex items-center justify-center gap-1.5">
              <CheckCircle2 className="w-3.5 h-3.5 text-slate-700" />
              <span>Append-Only Audit</span>
            </div>
          </div>

          {/* Case Dossier Live Container */}
          <div className="mt-14 max-w-5xl mx-auto rounded-2xl border border-slate-200/90 bg-white shadow-[0_20px_60px_-15px_rgba(15,23,42,0.12)] overflow-hidden text-left transition-all">
            {/* Case Dossier Header Bar */}
            <div className="bg-slate-900 px-5 py-3.5 border-b border-slate-800 flex items-center justify-between text-white">
              <div className="flex items-center gap-3">
                <span className="text-xs font-mono font-medium text-slate-300">
                  SURVEILLANCE DOSSIER
                </span>
                <span className="text-slate-600">/</span>
                <span className="text-xs font-mono text-slate-200 bg-slate-800 border border-slate-700 px-2 py-0.5 rounded">
                  CASE-88192
                </span>
              </div>
              <div className="flex items-center gap-3 text-xs font-mono text-slate-400">
                <span className="inline-flex items-center gap-1 text-slate-400">
                  <Lock className="w-3 h-3 text-slate-400" />
                  <span>TreeSHAP Grounded</span>
                </span>
              </div>
            </div>

            {/* Window Content */}
            <div className="p-6 sm:p-8 grid grid-cols-1 lg:grid-cols-3 gap-6 bg-[#fcfbf9]">
              <div className="lg:col-span-2 space-y-5">
                <div className="flex items-start justify-between">
                  <div>
                    <div className="text-[11px] font-mono uppercase tracking-wider text-slate-400">
                      CASE DOSSIER #INV-88192
                    </div>
                    <div className="text-xl sm:text-2xl font-semibold text-slate-900 mt-0.5">
                      International Wire Deviation ($84,500.00 USD)
                    </div>
                  </div>
                  <RiskBadge level="critical" score={87.5} />
                </div>

                <div className="grid grid-cols-3 gap-3 p-3.5 bg-white border border-slate-200/80 rounded-xl shadow-2xs">
                  <div>
                    <div className="text-[11px] text-slate-400 font-medium">Origination Entity</div>
                    <div className="text-xs font-semibold text-slate-800 mt-0.5">ACC-100482 (Apex Global)</div>
                  </div>
                  <div>
                    <div className="text-[11px] text-slate-400 font-medium">Corridor Analysis</div>
                    <div className="text-xs font-semibold text-slate-800 mt-0.5">KY (Offshore Routing)</div>
                  </div>
                  <div>
                    <div className="text-[11px] text-slate-400 font-medium">Supervised XGBoost</div>
                    <div className="text-xs font-mono font-semibold text-red-600 mt-0.5">0.88 Prob (Critical)</div>
                  </div>
                </div>

                {/* TreeSHAP Contributing Drivers */}
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-xs font-semibold text-slate-800 uppercase tracking-wider">
                    <span>Native TreeSHAP Feature Attributions</span>
                    <span className="text-[10px] font-mono text-slate-400 lowercase">mathematical attribution</span>
                  </div>
                  <div className="space-y-2 text-xs">
                    <div className="flex items-center justify-between p-2.5 bg-orange-50/70 border border-orange-200/70 rounded-lg">
                      <span className="text-slate-800 font-medium">
                        Amount $84,500.00 deviates significantly from 30-day baseline
                      </span>
                      <span className="font-mono font-semibold text-orange-700 bg-orange-100/70 px-2 py-0.5 rounded">
                        +0.42 SHAP
                      </span>
                    </div>
                    <div className="flex items-center justify-between p-2.5 bg-orange-50/70 border border-orange-200/70 rounded-lg">
                      <span className="text-slate-800 font-medium">
                        Unfamiliar cross-border destination corridor detected
                      </span>
                      <span className="font-mono font-semibold text-orange-700 bg-orange-100/70 px-2 py-0.5 rounded">
                        +0.31 SHAP
                      </span>
                    </div>
                    <div className="flex items-center justify-between p-2.5 bg-emerald-50/70 border border-emerald-200/70 rounded-lg">
                      <span className="text-slate-700 font-medium">
                        Known corporate network authentication credentials verified
                      </span>
                      <span className="font-mono font-semibold text-emerald-700 bg-emerald-100/70 px-2 py-0.5 rounded">
                        -0.08 SHAP
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Right Panel: Grounded AI Copilot & Human Sign-Off Notice */}
              <div className="border-t lg:border-t-0 lg:border-l border-slate-200 pt-5 lg:pt-0 lg:pl-6 space-y-4 flex flex-col justify-between">
                <div>
                  <div className="text-xs font-semibold text-slate-800 uppercase tracking-wider mb-2">
                    Grounded AI Guidance
                  </div>
                  <div className="p-4 bg-white border border-slate-200 rounded-xl shadow-2xs space-y-2.5 text-xs">
                    <div className="font-semibold text-blue-900 flex items-center gap-1.5">
                      <FileText className="w-3.5 h-3.5 text-blue-600" />
                      <span>Citation: SOP-104 (Wire Verification)</span>
                    </div>
                    <p className="text-slate-600 leading-relaxed">
                      Wires exceeding $25,000 to offshore corridors require secondary authorization and confirmation with corporate controller before release.
                    </p>
                    <div className="text-[11px] font-mono text-emerald-700 font-medium flex items-center gap-1">
                      <CheckCircle2 className="w-3 h-3 text-emerald-600" />
                      <span>Grounded Citation • Zero Hallucination</span>
                    </div>
                  </div>
                </div>

                <div className="p-3.5 bg-slate-100/80 border border-slate-200/80 rounded-xl text-xs space-y-1">
                  <div className="font-semibold text-slate-800">Human-In-The-Loop Clearance</div>
                  <p className="text-slate-500 text-[11px]">
                    Action required by certified risk officer. Every state change is sealed in the append-only audit ledger.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Four Pillars Section (Bento Grid) */}
        <section id="capabilities" className="py-20 px-4 sm:px-6 lg:px-8 max-w-6xl mx-auto border-t border-slate-200/70">
          <div className="max-w-2xl mb-12">
            <h2 className="text-xs font-mono uppercase tracking-widest text-slate-500 mb-2">Platform Capabilities</h2>
            <h3 className="text-2xl sm:text-3xl font-semibold text-slate-900 tracking-tight">
              Designed around the analyst workflow, not arbitrary AI assertions.
            </h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="p-6 bg-white border border-slate-200/80 rounded-2xl shadow-2xs hover:shadow-md hover:-translate-y-1 transition-all duration-300 space-y-3.5">
              <div className="w-9 h-9 rounded-xl bg-slate-100 text-slate-800 flex items-center justify-center font-bold text-xs border border-slate-200">
                01
              </div>
              <h4 className="text-base font-semibold text-slate-900">Multi-Model Detect</h4>
              <p className="text-xs text-slate-600 leading-relaxed">
                Supervised classification with XGBoost coupled with Isolation Forest unsupervised anomaly scoring across 17 behavioral dimensions.
              </p>
            </div>

            <div className="p-6 bg-white border border-slate-200/80 rounded-2xl shadow-2xs hover:shadow-md hover:-translate-y-1 transition-all duration-300 space-y-3.5">
              <div className="w-9 h-9 rounded-xl bg-slate-100 text-slate-800 flex items-center justify-center font-bold text-xs border border-slate-200">
                02
              </div>
              <h4 className="text-base font-semibold text-slate-900">Explainable SHAP</h4>
              <p className="text-xs text-slate-600 leading-relaxed">
                Mathematical feature attribution breaking down the exact drivers behind every flagged transaction, eliminating black-box opacity.
              </p>
            </div>

            <div className="p-6 bg-white border border-slate-200/80 rounded-2xl shadow-2xs hover:shadow-md hover:-translate-y-1 transition-all duration-300 space-y-3.5">
              <div className="w-9 h-9 rounded-xl bg-slate-100 text-slate-800 flex items-center justify-center font-bold text-xs border border-slate-200">
                03
              </div>
              <h4 className="text-base font-semibold text-slate-900">Grounded Investigation</h4>
              <p className="text-xs text-slate-600 leading-relaxed">
                AI investigation assistant retrieving approved standard operating procedures and compliance policies with pgvector vector search.
              </p>
            </div>

            <div className="p-6 bg-white border border-slate-200/80 rounded-2xl shadow-2xs hover:shadow-md hover:-translate-y-1 transition-all duration-300 space-y-3.5">
              <div className="w-9 h-9 rounded-xl bg-slate-100 text-slate-800 flex items-center justify-center font-bold text-xs border border-slate-200">
                04
              </div>
              <h4 className="text-base font-semibold text-slate-900">Human Sign-Off & Audit</h4>
              <p className="text-xs text-slate-600 leading-relaxed">
                Clear, Escalate, or Confirm decisions logged directly to an append-only audit trail recording user identity, timestamp, and rationale.
              </p>
            </div>
          </div>
        </section>

        {/* Interactive Architecture Showcase with Neat Annotations */}
        <ArchitectureShowcase />


        {/* Explainability Deep Dive Section */}
        <section id="explainability" className="py-20 px-4 sm:px-6 lg:px-8 max-w-6xl mx-auto border-t border-slate-200/70">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-10 items-center">
            <div className="space-y-4">
              <h2 className="text-xs font-mono uppercase tracking-widest text-slate-500">Explainable Intelligence</h2>
              <h3 className="text-3xl font-semibold text-slate-900 tracking-tight">
                Why NIST principles demand explainability over opaque scores.
              </h3>
              <p className="text-sm text-slate-600 leading-relaxed font-normal">
                Regulators and compliance teams cannot act on black-box risk predictions. FinGuard AI translates complex machine learning inferences into clear mathematical feature attributions with TreeSHAP, showing analysts precisely why a transaction was flagged.
              </p>
              <div className="space-y-2.5 pt-2">
                <div className="flex items-start gap-2.5 text-xs text-slate-700">
                  <CheckCircle2 className="w-4 h-4 text-slate-700 mt-0.5 shrink-0" />
                  <span>Directional SHAP attributions explaining risk increase vs mitigation.</span>
                </div>
                <div className="flex items-start gap-2.5 text-xs text-slate-700">
                  <CheckCircle2 className="w-4 h-4 text-slate-700 mt-0.5 shrink-0" />
                  <span>Rule engine findings combined with model outputs for clear reasoning.</span>
                </div>
                <div className="flex items-start gap-2.5 text-xs text-slate-700">
                  <CheckCircle2 className="w-4 h-4 text-slate-700 mt-0.5 shrink-0" />
                  <span>RAG AI assistant grounded strictly in verified compliance documents.</span>
                </div>
              </div>
            </div>

            <div className="p-6 bg-white border border-slate-200 rounded-2xl shadow-sm space-y-4">
              <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                <span className="text-xs font-semibold text-slate-800">Legacy AI vs FinGuard AI</span>
                <span className="text-[10px] font-mono text-slate-400">Comparison Matrix</span>
              </div>

              <div className="p-3 bg-red-50/60 border border-red-200/60 rounded-xl space-y-1">
                <div className="text-xs font-semibold text-red-900">Traditional Black-Box AI</div>
                <div className="text-xs text-red-700">
                  Outputs single raw score (e.g. 0.89) without breakdown. Analyst cannot explain reason to auditor.
                </div>
              </div>

              <div className="p-3 bg-emerald-50/60 border border-emerald-200/60 rounded-xl space-y-1">
                <div className="text-xs font-semibold text-emerald-900">FinGuard TreeSHAP Intelligence</div>
                <div className="text-xs text-emerald-800">
                  Quantifies exact percentage and feature contributors. Grounded RAG cites applicable operating procedure.
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Governance & CTA Section */}
        <section id="governance" className="py-24 px-4 sm:px-6 lg:px-8 max-w-6xl mx-auto border-t border-slate-200/70">
          <div className="max-w-3xl mx-auto text-center space-y-6">
            <h2 className="text-3xl sm:text-4xl font-semibold text-slate-900 tracking-tight">
              Experience explainable risk intelligence in action.
            </h2>
            <p className="text-sm text-slate-600 max-w-xl mx-auto leading-relaxed">
              Walk through real-time transaction ingestion, alert generation, TreeSHAP feature attributions, and analyst case sign-off in the sandbox runbook.
            </p>
            <div className="flex items-center justify-center gap-3.5 pt-2">
              <Link
                href="/demo"
                className="px-6 py-3 rounded-full bg-slate-900 text-white font-semibold text-sm hover:bg-slate-800 transition-all shadow-md shadow-slate-900/20 hover:scale-[1.02]"
              >
                Launch Interactive Demo
              </Link>
              <Link
                href="/sign-in"
                className="px-6 py-3 rounded-full bg-white border border-slate-200 text-slate-800 font-semibold text-sm hover:bg-slate-50 transition-all shadow-sm"
              >
                Analyst Sign In
              </Link>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}
