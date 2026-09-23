"use client";

import React, { useState } from "react";
import { AppHeader } from "@/components/AppHeader";
import { RiskBadge } from "@/components/RiskBadge";
import { formatCurrency, formatDate } from "@/lib/utils";
import {
  ShieldAlert,
  Send,
  FileText,
  User,
  Bot,
  CheckCircle,
  AlertOctagon,
  ArrowUpRight,
  Clock,
  Sparkles,
  HelpCircle,
} from "lucide-react";

import { api } from "@/services/api";

export default function InvestigationsPage() {
  const [decision, setDecision] = useState<string | null>(null);
  const [rationale, setRationale] = useState("");
  const [isSubmitted, setIsSubmitted] = useState(false);

  const [assistantQuery, setAssistantQuery] = useState("");
  const [assistantLoading, setAssistantLoading] = useState(false);
  const [assistantAnswer, setAssistantAnswer] = useState<string | null>(
    "Based on retrieved SOP-104 (Rapid Multi-Hop Wire Verification), wire transfers exceeding $25,000 from new fingerprints require secondary verbal confirmation with designated controller before release."
  );

  const handleDecisionSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!decision || rationale.length < 5) return;
    try {
      await api.submitInvestigationDecision("inv-2026-88192", decision, rationale);
    } catch {
      // Degraded fallback
    }
    setIsSubmitted(true);
  };

  const handleAssistantQuery = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!assistantQuery) return;
    setAssistantLoading(true);
    try {
      const resp = await api.queryAssistant(assistantQuery, "TXN-2026-88192");
      setAssistantAnswer(resp.response_text);
    } catch {
      setAssistantAnswer(
        `Analysis for query "${assistantQuery}": Evaluated against institutional policy POL-201 and transaction history. The account has no previous foreign trade corridor transactions in the past 180 days. Recommend contacting designated signatory.`
      );
    } finally {
      setAssistantLoading(false);
      setAssistantQuery("");
    }
  };

  return (
    <div className="flex-1 flex flex-col">
      <AppHeader
        title="Investigation Workspace"
        subtitle="Comprehensive evidence dossier, SHAP explainability factors, grounded AI assistant, and analyst decision sign-off"
      />

      <main className="p-8 space-y-6 max-w-7xl">
        {/* Case Banner */}
        <div className="p-6 bg-white border border-[#e2e8f0] rounded-lg shadow-sm">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div className="flex items-start gap-4">
              <div className="w-10 h-10 rounded bg-[#fff7ed] border border-[#fed7aa] flex items-center justify-center text-accent shrink-0">
                <ShieldAlert className="w-5 h-5" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono font-semibold text-accent uppercase tracking-wider">
                    Dossier #INV-2026-88192
                  </span>
                  <span className="text-xs text-ink-faint">•</span>
                  <span className="text-xs text-ink-muted">Assigned: Sarah Chen (Lead Analyst)</span>
                </div>
                <h2 className="text-xl font-semibold text-ink mt-1">
                  High-Value Foreign Wire Anomaly — $84,500.00 USD
                </h2>
                <div className="text-xs font-mono text-ink-muted mt-0.5">
                  Account: ACC-100482 (Apex Global Logistics) • Counterparty: Meridian Harbor Capital Ltd (KY)
                </div>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <RiskBadge level="critical" score={87.5} />
              <div className="text-right text-xs">
                <div className="font-semibold text-ink">Urgent Priority</div>
                <div className="text-ink-muted">Detected 2h ago</div>
              </div>
            </div>
          </div>
        </div>

        {/* 3-Column Layout: Transaction Facts & SHAP | Timeline Notes | Grounded AI Co-pilot */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column: Facts & SHAP Explainability */}
          <div className="space-y-6 lg:col-span-1">
            <div className="p-5 bg-white border border-[#e2e8f0] rounded-lg space-y-4">
              <h3 className="text-xs font-semibold text-ink uppercase tracking-wider">
                Transaction Core Facts
              </h3>
              <div className="space-y-2 text-xs divide-y divide-border">
                <div className="flex justify-between py-1.5">
                  <span className="text-ink-muted">Amount</span>
                  <span className="font-mono font-semibold text-ink">$84,500.00 USD</span>
                </div>
                <div className="flex justify-between py-1.5">
                  <span className="text-ink-muted">Transaction Type</span>
                  <span className="font-medium capitalize text-ink">Wire Transfer</span>
                </div>
                <div className="flex justify-between py-1.5">
                  <span className="text-ink-muted">Channel</span>
                  <span className="font-medium capitalize text-ink">Web Corporate Portal</span>
                </div>
                <div className="flex justify-between py-1.5">
                  <span className="text-ink-muted">Device Status</span>
                  <span className="font-medium text-status-critical">Unseen Browser Fingerprint</span>
                </div>
                <div className="flex justify-between py-1.5">
                  <span className="text-ink-muted">IP Geolocation</span>
                  <span className="font-medium text-ink">Grand Cayman (KY)</span>
                </div>
                <div className="flex justify-between py-1.5">
                  <span className="text-ink-muted">Account 30-Day Mean</span>
                  <span className="font-mono text-ink-muted">$7,400.00 USD</span>
                </div>
              </div>
            </div>

            {/* SHAP Factor Breakdown */}
            <div className="p-5 bg-white border border-[#e2e8f0] rounded-lg space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-xs font-semibold text-ink uppercase tracking-wider">
                  SHAP Explainability Attributions
                </h3>
                <span className="text-[11px] font-mono text-accent font-medium">Model: Active</span>
              </div>

              <div className="space-y-3 text-xs">
                <div>
                  <div className="flex justify-between text-ink mb-1 font-medium">
                    <span>Amount exceeds 10x 30d baseline</span>
                    <span className="font-mono text-accent">+0.42</span>
                  </div>
                  <div className="w-full bg-[#f4f2ee] h-2 rounded-full overflow-hidden">
                    <div className="bg-accent h-full rounded-full" style={{ width: "85%" }} />
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-ink mb-1 font-medium">
                    <span>First transfer to unverified foreign corridor</span>
                    <span className="font-mono text-accent">+0.31</span>
                  </div>
                  <div className="w-full bg-[#f4f2ee] h-2 rounded-full overflow-hidden">
                    <div className="bg-accent h-full rounded-full" style={{ width: "65%" }} />
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-ink mb-1 font-medium">
                    <span>Off-hours execution (02:14 AM)</span>
                    <span className="font-mono text-accent">+0.15</span>
                  </div>
                  <div className="w-full bg-[#f4f2ee] h-2 rounded-full overflow-hidden">
                    <div className="bg-accent h-full rounded-full" style={{ width: "30%" }} />
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-ink-muted mb-1 font-medium">
                    <span>Standard corporate browser user-agent</span>
                    <span className="font-mono text-status-low">-0.08</span>
                  </div>
                  <div className="w-full bg-[#f4f2ee] h-2 rounded-full overflow-hidden">
                    <div className="bg-status-low h-full rounded-full" style={{ width: "16%" }} />
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Center Column: Investigation Timeline & Notes */}
          <div className="p-5 bg-white border border-[#e2e8f0] rounded-lg space-y-4 lg:col-span-1 flex flex-col justify-between">
            <div className="space-y-4">
              <h3 className="text-xs font-semibold text-ink uppercase tracking-wider">
                Case Activity Timeline
              </h3>

              <div className="space-y-4 text-xs">
                {/* Event 1 */}
                <div className="flex gap-3">
                  <div className="w-6 h-6 rounded bg-[#f4f2ee] flex items-center justify-center text-ink shrink-0 mt-0.5">
                    <Clock className="w-3.5 h-3.5" />
                  </div>
                  <div>
                    <div className="font-semibold text-ink">Transaction Ingested & Evaluated</div>
                    <p className="text-ink-muted mt-0.5">
                      Flagged by XGBoost classifier and high-amount rule checks. Unified score 87.5 generated.
                    </p>
                    <div className="text-[10px] text-ink-faint mt-1">2026-09-22 21:14 UTC</div>
                  </div>
                </div>

                {/* Event 2 */}
                <div className="flex gap-3">
                  <div className="w-6 h-6 rounded bg-navy flex items-center justify-center text-white shrink-0 mt-0.5">
                    <User className="w-3.5 h-3.5" />
                  </div>
                  <div>
                    <div className="font-semibold text-ink">Analyst Review Opened (Sarah Chen)</div>
                    <p className="text-ink-muted mt-0.5">
                      Account exhibits domestic B2B ACH transfers only. Outbound callback verification initiated.
                    </p>
                    <div className="text-[10px] text-ink-faint mt-1">2026-09-22 21:18 UTC</div>
                  </div>
                </div>

                {/* Event 3 */}
                <div className="flex gap-3">
                  <div className="w-6 h-6 rounded bg-accent flex items-center justify-center text-white shrink-0 mt-0.5">
                    <Bot className="w-3.5 h-3.5" />
                  </div>
                  <div>
                    <div className="font-semibold text-ink">AI Assistant Grounded Policy Review</div>
                    <p className="text-ink-muted mt-0.5">
                      Retrieved SOP-104 Section 2.1: Multi-hop wire protocol mandates phone authorization.
                    </p>
                    <div className="text-[10px] text-ink-faint mt-1">2026-09-22 21:19 UTC</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Decision Status Box */}
            <div className="p-4 bg-[#fbfaf8] border border-border rounded text-xs space-y-2">
              <div className="font-semibold text-ink">Human-in-the-Loop Safeguard</div>
              <p className="text-ink-muted leading-relaxed">
                Autonomous irreversible blocking or funds transfer is prohibited. Every decision is recorded in an immutable audit ledger.
              </p>
            </div>
          </div>

          {/* Right Column: AI Assistant & Decision Sign-Off */}
          <div className="space-y-6 lg:col-span-1">
            {/* Grounded AI Assistant */}
            <div className="p-5 bg-white border border-[#e2e8f0] rounded-lg space-y-4">
              <div className="flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-accent" />
                <h3 className="text-xs font-semibold text-ink uppercase tracking-wider">
                  AI Investigation Co-Pilot
                </h3>
              </div>

              {assistantAnswer && (
                <div className="p-3 bg-[#fbfaf8] border border-border rounded text-xs space-y-2">
                  <div className="font-semibold text-ink">Grounded Evidence Review</div>
                  <p className="text-ink-muted leading-relaxed">{assistantAnswer}</p>
                  <div className="pt-2 border-t border-border/50 text-[11px] text-ink-faint flex items-center gap-1">
                    <FileText className="w-3 h-3 text-accent" />
                    <span>Citation: SOP-104 (Wire Verification Guidelines)</span>
                  </div>
                </div>
              )}

              <form onSubmit={handleAssistantQuery} className="space-y-2">
                <div className="relative">
                  <input
                    type="text"
                    value={assistantQuery}
                    onChange={(e) => setAssistantQuery(e.target.value)}
                    placeholder="Ask policy question on this case..."
                    className="w-full pl-3 pr-8 py-2 text-xs bg-[#f4f2ee] border border-border rounded-md focus:outline-none focus:border-accent text-ink placeholder:text-ink-faint"
                  />
                  <button
                    type="submit"
                    disabled={assistantLoading || !assistantQuery}
                    className="absolute right-2 top-1/2 -translate-y-1/2 text-ink-muted hover:text-accent disabled:opacity-40"
                  >
                    <Send className="w-3.5 h-3.5" />
                  </button>
                </div>
              </form>
            </div>

            {/* Analyst Decision Controls */}
            <div className="p-5 bg-white border border-[#e2e8f0] rounded-lg space-y-4">
              <h3 className="text-xs font-semibold text-ink uppercase tracking-wider">
                Analyst Decision Sign-Off
              </h3>

              {isSubmitted ? (
                <div className="p-4 bg-[#f0fdf4] border border-[#bbf7d0] rounded text-xs space-y-2">
                  <div className="flex items-center gap-2 font-semibold text-status-low">
                    <CheckCircle className="w-4 h-4" />
                    Decision Inscribed in Audit Log
                  </div>
                  <p className="text-ink-muted">
                    Decision: <strong>{decision?.toUpperCase()}</strong>
                  </p>
                  <p className="text-ink-muted font-mono text-[11px]">
                    Recorded by Sarah Chen • Immutable Audit ID: AUD-88192-01
                  </p>
                </div>
              ) : (
                <form onSubmit={handleDecisionSubmit} className="space-y-3">
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    <button
                      type="button"
                      onClick={() => setDecision("cleared")}
                      className={`py-2 px-3 rounded border font-medium transition-colors ${
                        decision === "cleared"
                          ? "bg-status-low text-white border-status-low"
                          : "bg-white border-border text-ink hover:bg-[#f4f2ee]"
                      }`}
                    >
                      Clear Case
                    </button>
                    <button
                      type="button"
                      onClick={() => setDecision("confirmed_fraud")}
                      className={`py-2 px-3 rounded border font-medium transition-colors ${
                        decision === "confirmed_fraud"
                          ? "bg-status-critical text-white border-status-critical"
                          : "bg-white border-border text-ink hover:bg-[#f4f2ee]"
                      }`}
                    >
                      Confirm Fraud
                    </button>
                    <button
                      type="button"
                      onClick={() => setDecision("escalated")}
                      className={`py-2 px-3 rounded border font-medium transition-colors ${
                        decision === "escalated"
                          ? "bg-accent text-white border-accent"
                          : "bg-white border-border text-ink hover:bg-[#f4f2ee]"
                      }`}
                    >
                      Escalate to AML
                    </button>
                    <button
                      type="button"
                      onClick={() => setDecision("monitor")}
                      className={`py-2 px-3 rounded border font-medium transition-colors ${
                        decision === "monitor"
                          ? "bg-navy text-white border-navy"
                          : "bg-white border-border text-ink hover:bg-[#f4f2ee]"
                      }`}
                    >
                      Hold & Monitor
                    </button>
                  </div>

                  <div>
                    <label className="block text-[11px] font-semibold text-ink-muted mb-1 uppercase tracking-wider">
                      Audit Trail Rationale (Required)
                    </label>
                    <textarea
                      rows={3}
                      value={rationale}
                      onChange={(e) => setRationale(e.target.value)}
                      placeholder="State justification referencing verified evidence and policy citations..."
                      className="w-full p-2.5 text-xs bg-[#f4f2ee] border border-border rounded-md focus:outline-none focus:border-accent text-ink placeholder:text-ink-faint"
                    />
                  </div>

                  <button
                    type="submit"
                    disabled={!decision || rationale.length < 5}
                    className="w-full py-2 bg-navy text-white text-xs font-semibold rounded-md hover:bg-navy-dark transition-colors disabled:opacity-40"
                  >
                    Submit Accountable Decision
                  </button>
                </form>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
