import React from "react";
import Link from "next/link";
import { AppHeader } from "@/components/AppHeader";
import { RiskBadge } from "@/components/RiskBadge";
import { api } from "@/services/api";
import { formatCurrency, formatDate } from "@/lib/utils";
import { AlertTriangle, ArrowUpRight, Check, X, ShieldAlert } from "lucide-react";

export default async function AlertsPage() {
  const { items: alerts = [] } = await api.getAlerts();

  return (
    <div className="flex-1 flex flex-col">
      <AppHeader
        title="Surveillance Alerts Queue"
        subtitle="Automated high-risk alerts flagged by XGBoost, Isolation Forest, and deterministic policy checks"
      />

      <main className="p-8 space-y-6 max-w-7xl">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-1 bg-navy text-white text-xs font-medium rounded-md">All Alerts ({alerts.length})</span>
            <span className="px-2.5 py-1 bg-white border border-border text-ink-muted text-xs font-medium rounded-md hover:text-ink cursor-pointer">
              Critical (2)
            </span>
            <span className="px-2.5 py-1 bg-white border border-border text-ink-muted text-xs font-medium rounded-md hover:text-ink cursor-pointer">
              High (5)
            </span>
          </div>

          <div className="text-xs text-ink-muted">
            Prioritized by Unified Risk Score
          </div>
        </div>

        <div className="space-y-3">
          {alerts.map((alert) => (
            <div
              key={alert.id}
              className="p-5 bg-white border border-[#e2e8f0] rounded-lg shadow-sm hover:border-accent/40 transition-colors space-y-4"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded bg-[#fff7ed] border border-[#fed7aa] flex items-center justify-center text-accent">
                    <ShieldAlert className="w-4 h-4" />
                  </div>
                  <div>
                    <div className="text-sm font-semibold text-ink">{alert.trigger_reason}</div>
                    <div className="text-xs font-mono text-ink-muted">
                      Tx: {alert.transaction_id} • Account: {alert.account_id} • Detected {formatDate(alert.created_at)}
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <RiskBadge level={alert.risk_level} score={alert.risk_score} />
                  <span className="px-2.5 py-0.5 rounded text-xs font-medium uppercase tracking-wider bg-[#f4f2ee] border border-border text-ink-muted">
                    {alert.status}
                  </span>
                </div>
              </div>

              {/* Factors Summary Preview */}
              {alert.factors_summary && (
                <div className="p-3 bg-[#fbfaf8] border border-border rounded text-xs space-y-1.5">
                  <div className="text-[11px] font-semibold text-ink uppercase tracking-wider">Top Detected Signals</div>
                  <div className="text-ink-muted leading-relaxed">
                    Transaction exhibits severe volume deviation and cross-border routing anomalies from account 30-day baseline.
                  </div>
                </div>
              )}

              <div className="flex items-center justify-between pt-2 border-t border-border text-xs">
                <div className="font-mono text-ink-muted">
                  Amount:{" "}
                  <span className="font-semibold text-ink">
                    {alert.transaction_amount ? formatCurrency(alert.transaction_amount, alert.transaction_currency) : "—"}
                  </span>
                </div>

                <div className="flex items-center gap-2">
                  <Link
                    href="/investigations"
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-accent text-white rounded text-xs font-medium hover:bg-accent-hover transition-colors shadow-sm"
                  >
                    Open Investigation Dossier <ArrowUpRight className="w-3.5 h-3.5" />
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
