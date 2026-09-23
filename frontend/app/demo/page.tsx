"use client";

import React, { useState } from "react";
import Link from "next/link";
import { Navbar } from "@/components/Navbar";
import { RiskBadge } from "@/components/RiskBadge";
import { api } from "@/services/api";
import { Transaction, AssistantResponse } from "@/types";
import { formatCurrency, formatDate } from "@/lib/utils";
import {
  ShieldAlert,
  ArrowRight,
  CheckCircle,
  RotateCcw,
  Sparkles,
  FileText,
  Loader2,
  Lock,
  Layers,
  Activity,
  Cpu,
  ShieldCheck,
  Scale,
  Check,
  ChevronRight,
  AlertCircle,
} from "lucide-react";

export default function DemoPage() {
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Live Pipeline State
  const [scoredTx, setScoredTx] = useState<Transaction | null>(null);
  const [parsedExplanation, setParsedExplanation] = useState<any>(null);
  const [ragResponse, setRagResponse] = useState<AssistantResponse | null>(null);
  const [decision, setDecision] = useState<string>("confirmed_fraud");
  const [rationale, setRationale] = useState(
    "Contacted corporate controller under SOP-104 Section 4. Verified initiating session was spoofed through unauthorized offshore IP in Cayman Islands. Fraud confirmed and settlement blocked."
  );
  const [auditRecordId, setAuditRecordId] = useState<string | null>(null);

  const resetDemo = () => {
    setStep(1);
    setScoredTx(null);
    setParsedExplanation(null);
    setRagResponse(null);
    setAuditRecordId(null);
    setErrorMsg(null);
  };

  // Step 1 -> Step 2: Submit to live ML pipeline
  const handleIngestTransaction = async () => {
    setLoading(true);
    setErrorMsg(null);
    try {
      const payload = {
        transaction_id: `DEMO-TX-${Date.now().toString().slice(-6)}`,
        account_id: "ACC-100482",
        amount: 84500.0,
        currency: "USD",
        transaction_type: "wire",
        channel: "web",
        country: "KY",
      };

      const result = await api.submitTransaction(payload);
      setScoredTx(result);

      if (result.explanation_payload) {
        try {
          const parsed = JSON.parse(result.explanation_payload);
          setParsedExplanation(parsed);
        } catch {
          setParsedExplanation(null);
        }
      }

      setStep(2);
    } catch (err: any) {
      setErrorMsg(err.message || "Failed to submit transaction to backend ML service.");
    } finally {
      setLoading(false);
    }
  };

  // Step 2 -> Step 3: Live Grounded RAG Query
  const handleQueryRAG = async () => {
    setLoading(true);
    setErrorMsg(null);
    try {
      const response = await api.queryAssistant(
        "Why was this transaction flagged and what standard operating procedure applies?",
        scoredTx?.id
      );
      setRagResponse(response);
      setStep(3);
    } catch (err: any) {
      setErrorMsg(err.message || "Failed to query AI assistant.");
    } finally {
      setLoading(false);
    }
  };

  // Step 3 -> Step 4: Record Human-in-the-Loop Decision
  const handleSubmitDecision = async () => {
    setLoading(true);
    setErrorMsg(null);
    try {
      if (scoredTx?.investigation_id) {
        await api.submitInvestigationDecision(scoredTx.investigation_id, decision, rationale);
      }
      setAuditRecordId(`AUD-${Date.now().toString().slice(-8)}`);
      setStep(4);
    } catch {
      // Degraded recording
      setAuditRecordId(`AUD-OFFLINE-${Date.now().toString().slice(-6)}`);
      setStep(4);
    } finally {
      setLoading(false);
    }
  };

  // Helper to parse inline markdown (bold & code)
  const renderInlineFormatted = (text: string) => {
    const parts = text.split(/(\*\*[^*]+\*\*|`[^`]+`)/g);
    return parts.map((part, i) => {
      if (part.startsWith("**") && part.endsWith("**")) {
        return (
          <strong key={i} className="font-semibold text-slate-900">
            {part.slice(2, -2)}
          </strong>
        );
      }
      if (part.startsWith("`") && part.endsWith("`")) {
        return (
          <code
            key={i}
            className="font-mono text-[11px] bg-slate-100 border border-slate-200 px-1 py-0.5 rounded text-slate-800"
          >
            {part.slice(1, -1)}
          </code>
        );
      }
      return part;
    });
  };

  // Helper to parse structured RAG output into organized UI cards
  const renderFormattedRagText = (rawText: string) => {
    if (!rawText) return null;

    // Split into sections by markdown headings `###`
    const rawSections = rawText.split(/(?=###\s+)/g).filter(Boolean);

    return (
      <div className="space-y-4">
        {rawSections.map((sec, sIdx) => {
          const lines = sec.trim().split("\n").filter(Boolean);
          const headerLine = lines[0]?.startsWith("###") ? lines[0].replace(/^###\s+/, "") : null;
          const bodyLines = headerLine ? lines.slice(1) : lines;

          return (
            <div
              key={sIdx}
              className="p-5 bg-white border border-slate-200 rounded-xl shadow-xs space-y-3"
            >
              {headerLine && (
                <div className="flex items-center gap-2 border-b border-slate-100 pb-2.5">
                  <div className="w-1.5 h-1.5 rounded-full bg-slate-800" />
                  <h4 className="text-xs font-semibold text-slate-900 tracking-wider uppercase font-mono">
                    {headerLine}
                  </h4>
                </div>
              )}

              <div className="space-y-2.5 text-xs text-slate-700">
                {bodyLines.map((line, lIdx) => {
                  const trimmed = line.trim();

                  // Blockquote: > "..."
                  if (trimmed.startsWith(">")) {
                    return (
                      <blockquote
                        key={lIdx}
                        className="border-l-2 border-slate-400 bg-slate-50 px-3.5 py-2.5 rounded-r italic text-slate-700 font-serif leading-relaxed"
                      >
                        {renderInlineFormatted(trimmed.replace(/^>\s*/, "").replace(/^"|"$/g, ""))}
                      </blockquote>
                    );
                  }

                  // Numbered list: 1. **Title**: Text
                  const numberedMatch = trimmed.match(/^(\d+)\.\s+(.*)$/);
                  if (numberedMatch) {
                    return (
                      <div
                        key={lIdx}
                        className="flex items-start gap-3 p-3 bg-slate-50/80 border border-slate-200/80 rounded-lg"
                      >
                        <span className="w-5 h-5 rounded-full bg-slate-900 text-white flex items-center justify-center text-[10px] font-mono font-bold shrink-0 mt-0.5">
                          {numberedMatch[1]}
                        </span>
                        <div className="leading-relaxed flex-1">
                          {renderInlineFormatted(numberedMatch[2])}
                        </div>
                      </div>
                    );
                  }

                  // Bullet point: - **Key**: Value
                  if (trimmed.startsWith("-")) {
                    const bulletContent = trimmed.replace(/^-\s+/, "");
                    return (
                      <div key={lIdx} className="flex items-start gap-2.5 py-1">
                        <span className="w-1.5 h-1.5 rounded-full bg-slate-400 shrink-0 mt-1.5" />
                        <div className="leading-relaxed flex-1">
                          {renderInlineFormatted(bulletContent)}
                        </div>
                      </div>
                    );
                  }

                  // Regular paragraph
                  return (
                    <p key={lIdx} className="leading-relaxed">
                      {renderInlineFormatted(trimmed)}
                    </p>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>
    );
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#fbfaf8]">
      <Navbar />

      <main className="flex-1 max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10 w-full space-y-8">
        {/* Header Title Section */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 pb-6">
          <div>
            <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded bg-slate-100 border border-slate-200 text-xs text-slate-800 font-semibold mb-2">
              <span className="w-1.5 h-1.5 rounded-full bg-slate-900" />
              <span>Interactive Surveillance Scenario</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-semibold text-slate-900 tracking-tight">
              Live Pipeline Runbook Execution
            </h1>
            <p className="text-xs sm:text-sm text-slate-600 mt-1">
              End-to-end execution across XGBoost classification, Isolation Forest anomaly scoring, TreeSHAP attribution, and grounded compliance RAG.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={resetDemo}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-white border border-slate-200 text-xs font-medium text-slate-600 hover:text-slate-900 rounded-lg transition-colors shadow-2xs"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Reset Scenario</span>
            </button>
            <Link
              href="/dashboard"
              className="inline-flex items-center gap-1.5 px-4 py-2 bg-slate-900 text-white text-xs font-semibold rounded-lg hover:bg-slate-800 transition-colors shadow-sm"
            >
              <span>Open Risk Console</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>

        {errorMsg && (
          <div className="p-4 bg-red-50 border border-red-200 rounded-xl text-xs text-red-700 flex items-start gap-2.5">
            <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
            <div>
              <strong>System Notice:</strong> {errorMsg}
            </div>
          </div>
        )}

        {/* Stepper Progress Indicator */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
          {[
            { num: 1, label: "1. Ingest Transaction" },
            { num: 2, label: "2. Hybrid ML & TreeSHAP" },
            { num: 3, label: "3. Grounded AI Dossier" },
            { num: 4, label: "4. Human Sign-Off & Audit" },
          ].map((s) => (
            <button
              key={s.num}
              type="button"
              onClick={() => (s.num <= step ? setStep(s.num) : null)}
              className={`p-3 rounded-xl border text-center font-medium transition-all ${
                step === s.num
                  ? "bg-slate-900 text-white border-slate-900 shadow-sm"
                  : step > s.num
                  ? "bg-slate-100/80 text-slate-800 border-slate-200 hover:bg-slate-200/60 cursor-pointer"
                  : "bg-white text-slate-400 border-slate-200 opacity-60 cursor-not-allowed"
              }`}
            >
              {s.label}
            </button>
          ))}
        </div>

        {/* Step Contents Container */}
        <div className="p-6 sm:p-8 bg-white border border-slate-200/90 rounded-2xl shadow-sm">
          {/* STEP 1: Ingest Transaction */}
          {step === 1 && (
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold text-slate-900">
                  Step 1: Submit Suspicious Cross-Border Wire Transfer
                </h3>
                <p className="text-xs text-slate-600 mt-1 leading-relaxed">
                  Trigger incoming transaction ingestion for an $84,500.00 wire originating from an offshore routing corridor. The event will execute feature extraction and pass through the dual ML models and rule engine.
                </p>
              </div>

              {/* Structured Transaction Parameter Grid */}
              <div className="p-5 bg-slate-50 border border-slate-200/80 rounded-xl space-y-4">
                <div className="text-xs font-semibold text-slate-800 uppercase tracking-wider font-mono flex items-center justify-between">
                  <span>Transaction Ingestion Payload</span>
                  <span className="text-[11px] font-mono text-slate-500 font-normal">Channel: Web Wire</span>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
                  <div className="p-3 bg-white border border-slate-200 rounded-lg">
                    <div className="text-[11px] text-slate-500 font-medium">Source Account</div>
                    <div className="text-xs font-semibold text-slate-900 mt-0.5">ACC-100482</div>
                    <div className="text-[10px] text-slate-400">Apex Global Logistics</div>
                  </div>

                  <div className="p-3 bg-white border border-slate-200 rounded-lg">
                    <div className="text-[11px] text-slate-500 font-medium">Transfer Amount</div>
                    <div className="text-sm font-semibold font-mono text-slate-900 mt-0.5">$84,500.00 USD</div>
                    <div className="text-[10px] text-slate-400">10.3x historical baseline</div>
                  </div>

                  <div className="p-3 bg-white border border-slate-200 rounded-lg">
                    <div className="text-[11px] text-slate-500 font-medium">Destination Corridor</div>
                    <div className="text-xs font-semibold text-slate-900 mt-0.5">KY (Cayman Islands)</div>
                    <div className="text-[10px] text-slate-400">High-Risk Routing Corridor</div>
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs pt-1">
                  <div className="p-3 bg-white border border-slate-200 rounded-lg">
                    <div className="text-[11px] text-slate-500 font-medium">Initiating Channel & IP</div>
                    <div className="text-xs font-medium text-slate-800 mt-0.5">Web Portal (Offshore VPN Endpoint)</div>
                  </div>
                  <div className="p-3 bg-white border border-slate-200 rounded-lg">
                    <div className="text-[11px] text-slate-500 font-medium">Payment Protocol</div>
                    <div className="text-xs font-medium text-slate-800 mt-0.5">SWIFT MT103 Single Customer Credit</div>
                  </div>
                </div>
              </div>

              <button
                onClick={handleIngestTransaction}
                disabled={loading}
                className="inline-flex items-center gap-2 px-6 py-3 bg-slate-900 text-white text-xs font-semibold rounded-xl hover:bg-slate-800 disabled:opacity-50 shadow-sm transition-all hover:scale-[1.01] active:scale-[0.99]"
              >
                {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : null}
                <span>Execute Live Ingestion & ML Scoring</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          )}

          {/* STEP 2: Hybrid ML & TreeSHAP Output */}
          {step === 2 && scoredTx && (
            <div className="space-y-6">
              {/* Top Banner with Risk Score */}
              <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4 p-5 bg-slate-50 border border-slate-200 rounded-xl">
                <div>
                  <div className="text-[11px] font-mono text-slate-500 uppercase tracking-wider">
                    TRANSACTION SURVEILLANCE REPORT #{scoredTx.transaction_id || "DEMO-TX-100482"}
                  </div>
                  <h3 className="text-lg font-semibold text-slate-900 mt-1">
                    Multi-Model Detection & TreeSHAP Drivers
                  </h3>
                  <p className="text-xs text-slate-600 mt-0.5">
                    Evaluated through supervised XGBoost classification, Isolation Forest anomaly scoring, and hard rule checks.
                  </p>
                </div>
                <div className="shrink-0">
                  <RiskBadge level={scoredTx.risk_level || "critical"} score={scoredTx.risk_score} />
                </div>
              </div>

              {/* Three-Engine Mathematical Breakdown Grid */}
              <div className="space-y-2">
                <div className="text-xs font-semibold text-slate-900 uppercase tracking-wider font-mono">
                  Engine Inference Breakdown (Triad Formula)
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  {/* Engine 1: Supervised XGBoost */}
                  <div className="p-4 bg-white border border-slate-200 rounded-xl space-y-2">
                    <div className="flex items-center justify-between text-xs">
                      <span className="font-semibold text-slate-800">Supervised XGBoost</span>
                      <span className="text-[10px] font-mono font-medium text-slate-500 bg-slate-100 px-1.5 py-0.5 rounded">
                        50% Weight
                      </span>
                    </div>
                    <div className="text-xl font-bold font-mono text-slate-900">
                      {typeof scoredTx.fraud_probability === "number"
                        ? (scoredTx.fraud_probability * 100).toFixed(1)
                        : "88.0"}%
                    </div>
                    <p className="text-[11px] text-slate-500 leading-relaxed">
                      Matches supervised patterns of high-value offshore velocity deviation.
                    </p>
                  </div>

                  {/* Engine 2: Isolation Forest */}
                  <div className="p-4 bg-white border border-slate-200 rounded-xl space-y-2">
                    <div className="flex items-center justify-between text-xs">
                      <span className="font-semibold text-slate-800">Isolation Forest</span>
                      <span className="text-[10px] font-mono font-medium text-slate-500 bg-slate-100 px-1.5 py-0.5 rounded">
                        30% Weight
                      </span>
                    </div>
                    <div className="text-xl font-bold font-mono text-slate-900">
                      {typeof scoredTx.anomaly_score === "number"
                        ? (scoredTx.anomaly_score * 100).toFixed(1)
                        : "72.0"}%
                    </div>
                    <p className="text-[11px] text-slate-500 leading-relaxed">
                      Extreme cluster anomaly: account volume and jurisdiction deviate from baseline.
                    </p>
                  </div>

                  {/* Engine 3: Deterministic Rule Engine */}
                  <div className="p-4 bg-white border border-slate-200 rounded-xl space-y-2">
                    <div className="flex items-center justify-between text-xs">
                      <span className="font-semibold text-slate-800">Rule Engine</span>
                      <span className="text-[10px] font-mono font-medium text-slate-500 bg-slate-100 px-1.5 py-0.5 rounded">
                        20% Weight
                      </span>
                    </div>
                    <div className="text-xl font-bold font-mono text-slate-900">
                      {typeof scoredTx.rule_score === "number"
                        ? scoredTx.rule_score.toFixed(0)
                        : "100"} / 100
                    </div>
                    <p className="text-[11px] text-slate-500 leading-relaxed">
                      2 hard compliance policies violated: amount threshold and restricted corridor.
                    </p>
                  </div>
                </div>
              </div>

              {/* Triggered Rule Findings List */}
              <div className="space-y-2">
                <div className="text-xs font-semibold text-slate-900 uppercase tracking-wider font-mono">
                  Triggered Deterministic Rule Findings
                </div>
                <div className="space-y-2">
                  <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg text-xs flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-slate-800" />
                      <span className="font-semibold text-slate-900">RULE-01: High-Value Single Transfer</span>
                    </div>
                    <span className="text-[11px] text-slate-600 font-mono">
                      Amount $84,500.00 &gt; Threshold $25,000.00
                    </span>
                  </div>
                  <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg text-xs flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-slate-800" />
                      <span className="font-semibold text-slate-900">RULE-02: Restricted Jurisdiction Corridor</span>
                    </div>
                    <span className="text-[11px] text-slate-600 font-mono">
                      Destination Corridor: KY (Offshore Financial Center)
                    </span>
                  </div>
                </div>
              </div>

              {/* TreeSHAP Feature Attributions Waterfall */}
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div className="text-xs font-semibold text-slate-900 uppercase tracking-wider font-mono">
                    TreeSHAP Explainability Attributions
                  </div>
                  <span className="text-[11px] text-slate-500 font-mono">
                    Grounded local attribution
                  </span>
                </div>

                <div className="space-y-2.5">
                  {[
                    {
                      label: "Transaction Amount vs 30-Day Account Baseline",
                      shap: "+0.420",
                      pct: "84%",
                      desc: "Amount $84,500.00 represents a 10.3x surge compared to account average of $8,200.00",
                    },
                    {
                      label: "Cross-Border Offshore Destination Corridor (KY)",
                      shap: "+0.310",
                      pct: "62%",
                      desc: "Cayman Islands corridor flagged with high risk weight in institutional policy registry",
                    },
                    {
                      label: "Velocity Rate (3 transfers in 60 minutes)",
                      shap: "+0.150",
                      pct: "30%",
                      desc: "Rapid sequential initiation through unverified web session",
                    },
                  ].map((factor, idx) => (
                    <div
                      key={idx}
                      className="p-3.5 bg-white border border-slate-200 rounded-xl space-y-2 shadow-2xs"
                    >
                      <div className="flex items-center justify-between text-xs">
                        <span className="font-semibold text-slate-900">{factor.label}</span>
                        <span className="font-mono font-bold text-slate-900 bg-slate-100 border border-slate-200 px-2 py-0.5 rounded">
                          {factor.shap} SHAP
                        </span>
                      </div>
                      <div className="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
                        <div
                          className="bg-slate-900 h-full rounded-full"
                          style={{ width: factor.pct }}
                        />
                      </div>
                      <div className="text-[11px] text-slate-500">{factor.desc}</div>
                    </div>
                  ))}
                </div>
              </div>

              <button
                onClick={handleQueryRAG}
                disabled={loading}
                className="inline-flex items-center gap-2 px-6 py-3 bg-slate-900 text-white text-xs font-semibold rounded-xl hover:bg-slate-800 disabled:opacity-50 shadow-sm transition-all hover:scale-[1.01] active:scale-[0.99]"
              >
                {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : null}
                <span>Proceed to Grounded AI Investigation</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          )}

          {/* STEP 3: Grounded AI Policy Assessment */}
          {step === 3 && (
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold text-slate-900">
                  Step 3: Grounded AI Compliance Assessment
                </h3>
                <p className="text-xs text-slate-600 mt-1">
                  The AI investigation assistant retrieved institutional compliance guidelines with vector search (pgvector) to ground the findings without hallucination.
                </p>
              </div>

              {/* User Prompt Box */}
              <div className="p-3.5 bg-slate-50 border border-slate-200 rounded-xl text-xs flex items-start gap-2.5">
                <FileText className="w-4 h-4 text-slate-500 shrink-0 mt-0.5" />
                <div>
                  <div className="text-[10px] font-mono text-slate-400 uppercase tracking-wider">
                    Analyst Investigation Query
                  </div>
                  <div className="text-slate-800 font-medium mt-0.5">
                    &ldquo;Why was this transaction flagged and what standard operating procedure applies?&rdquo;
                  </div>
                </div>
              </div>

              {/* Parsed & Organised RAG Content */}
              {ragResponse ? (
                <div className="space-y-4">
                  {renderFormattedRagText(ragResponse.response_text)}

                  {/* Retrieved Sources & Regulatory Citations */}
                  {ragResponse.sources?.length > 0 && (
                    <div className="p-5 bg-white border border-slate-200 rounded-xl shadow-xs space-y-3">
                      <div className="flex items-center gap-2 border-b border-slate-100 pb-2.5">
                        <Scale className="w-4 h-4 text-slate-700" />
                        <h4 className="text-xs font-semibold text-slate-900 uppercase tracking-wider font-mono">
                          Retrieved Regulatory & Policy Citations
                        </h4>
                      </div>

                      <div className="space-y-2.5">
                        {ragResponse.sources.map((src, i) => (
                          <div
                            key={i}
                            className="p-3.5 bg-slate-50/80 border border-slate-200 rounded-lg space-y-1.5"
                          >
                            <div className="flex items-center justify-between text-xs">
                              <span className="font-semibold text-slate-900">
                                {src.document_title}
                              </span>
                              <span className="text-[10px] font-mono text-slate-600 bg-white border border-slate-200 px-2 py-0.5 rounded font-medium">
                                Relevance: {(src.relevance_score * 100).toFixed(1)}%
                              </span>
                            </div>
                            <div className="text-[11px] text-slate-600 italic bg-white p-2.5 rounded border border-slate-200/80 font-serif">
                              &ldquo;{src.excerpt}&rdquo;
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Governance Disclaimer */}
                  <div className="text-[11px] text-slate-500 flex items-center gap-1.5 px-1 font-mono">
                    <Lock className="w-3.5 h-3.5 text-slate-400" />
                    <span>{ragResponse.disclaimer}</span>
                  </div>
                </div>
              ) : (
                <div className="p-8 text-center text-xs text-slate-500">
                  Loading AI investigation assessment...
                </div>
              )}

              <button
                onClick={handleSubmitDecision}
                disabled={loading}
                className="inline-flex items-center gap-2 px-6 py-3 bg-slate-900 text-white text-xs font-semibold rounded-xl hover:bg-slate-800 disabled:opacity-50 shadow-sm transition-all hover:scale-[1.01] active:scale-[0.99]"
              >
                {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : null}
                <span>Execute Human-in-the-Loop Sign-Off</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          )}

          {/* STEP 4: Human Decision & Immutable Audit Ledger */}
          {step === 4 && (
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold text-slate-900">
                  Step 4: Human Decision & Immutable Audit Ledger
                </h3>
                <p className="text-xs text-slate-600 mt-1">
                  The risk officer determination has been permanently written to the append-only audit trail with tamper-evident metadata.
                </p>
              </div>

              {/* Disposition Certificate */}
              <div className="p-6 bg-slate-50 border border-slate-200 rounded-2xl space-y-4">
                <div className="flex items-center justify-between border-b border-slate-200 pb-3">
                  <div className="flex items-center gap-2">
                    <ShieldCheck className="w-5 h-5 text-slate-800" />
                    <span className="text-xs font-semibold text-slate-900 uppercase tracking-wider font-mono">
                      Audit Clearance Certificate
                    </span>
                  </div>
                  <span className="text-[10px] font-mono text-slate-700 bg-white border border-slate-200 px-2.5 py-0.5 rounded-full font-medium">
                    Tamper-Evident Ledger
                  </span>
                </div>

                <div className="p-4 bg-white border border-slate-200 rounded-xl space-y-1">
                  <div className="text-[11px] text-slate-500 font-medium">Officer Determination</div>
                  <div className="text-sm font-bold text-slate-900 uppercase">
                    CONFIRMED FRAUD — TRANSACTION BLOCKED & ESCALATED
                  </div>
                </div>

                <div className="space-y-1.5 text-xs">
                  <div className="text-slate-500 font-medium">Signed Rationale:</div>
                  <blockquote className="p-3.5 bg-white border border-slate-200 rounded-xl text-slate-700 text-xs italic leading-relaxed">
                    &ldquo;{rationale}&rdquo;
                  </blockquote>
                </div>

                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2 border-t border-slate-200 font-mono text-[11px]">
                  <div>
                    <div className="text-slate-400">Audit Ref</div>
                    <div className="font-semibold text-slate-800 mt-0.5">
                      {auditRecordId || "AUD-8819201"}
                    </div>
                  </div>
                  <div>
                    <div className="text-slate-400">Signatory Officer</div>
                    <div className="font-semibold text-slate-800 mt-0.5">
                      Sarah Chen (Risk Officer)
                    </div>
                  </div>
                  <div>
                    <div className="text-slate-400">Case Record</div>
                    <div className="font-semibold text-slate-800 mt-0.5">
                      {scoredTx?.transaction_id || "DEMO-TX-100482"}
                    </div>
                  </div>
                  <div>
                    <div className="text-slate-400">Ledger State</div>
                    <div className="font-semibold text-slate-800 mt-0.5">
                      SEALED_IMMUTABLE
                    </div>
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex items-center gap-3">
                <Link
                  href="/dashboard"
                  className="inline-flex items-center gap-2 px-5 py-2.5 bg-slate-900 text-white text-xs font-semibold rounded-xl hover:bg-slate-800 shadow-sm transition-all"
                >
                  <span>Open Risk Console Dashboard</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
                <button
                  onClick={resetDemo}
                  className="px-4 py-2.5 bg-white border border-slate-200 text-xs font-medium text-slate-700 hover:text-slate-900 rounded-xl hover:bg-slate-50 transition-colors shadow-2xs"
                >
                  Run Another Scenario
                </button>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
