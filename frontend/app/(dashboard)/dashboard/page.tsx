import React from "react";
import Link from "next/link";
import { AppHeader } from "@/components/AppHeader";
import { RiskBadge } from "@/components/RiskBadge";
import { api } from "@/services/api";
import { formatCurrency, formatDate } from "@/lib/utils";
import { ArrowRight, AlertTriangle, ShieldCheck, Clock, Activity, ArrowUpRight } from "lucide-react";

export default async function DashboardPage() {
  const metrics = await api.getOverviewMetrics();
  const { items: alerts = [] } = await api.getAlerts();
  const { items: transactions = [] } = await api.getTransactions();
  const trends = await api.getRiskTrends();

  return (
    <div className="flex-1 flex flex-col">
      <AppHeader
        title="Operational Risk Overview"
        subtitle="Real-time transaction surveillance, anomaly detection, and triage queue"
      />

      <main className="p-8 space-y-8 max-w-7xl">
        {/* Metric Cards Row */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="p-5 bg-white border border-[#e2e8f0] rounded-lg">
            <div className="flex items-center justify-between text-xs text-ink-muted mb-2 font-medium">
              <span>Transactions (24h)</span>
              <Activity className="w-4 h-4 text-ink-faint" />
            </div>
            <div className="text-2xl font-semibold text-ink font-mono">
              {metrics.total_transactions_24h.toLocaleString()}
            </div>
            <div className="text-[11px] text-status-low mt-1 font-medium">Surveillance active across 5 channels</div>
          </div>

          <div className="p-5 bg-white border border-[#e2e8f0] rounded-lg">
            <div className="flex items-center justify-between text-xs text-ink-muted mb-2 font-medium">
              <span>Active Alerts</span>
              <AlertTriangle className="w-4 h-4 text-accent" />
            </div>
            <div className="text-2xl font-semibold text-ink font-mono">
              {metrics.active_alerts_count}
            </div>
            <div className="text-[11px] text-accent mt-1 font-medium">
              {metrics.critical_risk_count} critical, {metrics.high_risk_count} high risk
            </div>
          </div>

          <div className="p-5 bg-white border border-[#e2e8f0] rounded-lg">
            <div className="flex items-center justify-between text-xs text-ink-muted mb-2 font-medium">
              <span>Pending Investigations</span>
              <ShieldCheck className="w-4 h-4 text-navy" />
            </div>
            <div className="text-2xl font-semibold text-ink font-mono">
              {metrics.pending_investigations}
            </div>
            <div className="text-[11px] text-ink-muted mt-1">Assigned across risk analyst team</div>
          </div>

          <div className="p-5 bg-white border border-[#e2e8f0] rounded-lg">
            <div className="flex items-center justify-between text-xs text-ink-muted mb-2 font-medium">
              <span>Mean Resolution Time</span>
              <Clock className="w-4 h-4 text-ink-faint" />
            </div>
            <div className="text-2xl font-semibold text-ink font-mono">
              {metrics.mean_resolution_hours}h
            </div>
            <div className="text-[11px] text-status-low mt-1 font-medium">{metrics.resolved_today} resolved today</div>
          </div>
        </div>

        {/* Risk Trend Visual Section */}
        <div className="p-6 bg-white border border-[#e2e8f0] rounded-lg">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-sm font-semibold text-ink">Risk Classification Distribution (Past 7 Days)</h2>
              <p className="text-xs text-ink-muted">Evaluated across supervised XGBoost and unsupervised Isolation Forest engines</p>
            </div>
            <span className="text-xs font-mono text-ink-faint">Daily Aggregation</span>
          </div>

          <div className="grid grid-cols-7 gap-3 pt-4 border-t border-border">
            {trends.map((t) => (
              <div key={t.timestamp_label} className="text-center space-y-2">
                <div className="h-32 flex flex-col justify-end items-center gap-1">
                  {/* Critical bar */}
                  <div
                    style={{ height: `${Math.max(4, t.critical_count * 8)}px` }}
                    className="w-full bg-status-critical rounded-t-sm"
                    title={`Critical: ${t.critical_count}`}
                  />
                  {/* High bar */}
                  <div
                    style={{ height: `${Math.max(4, t.high_count * 3)}px` }}
                    className="w-full bg-accent"
                    title={`High: ${t.high_count}`}
                  />
                  {/* Medium bar */}
                  <div
                    style={{ height: `${Math.max(6, t.medium_count * 0.4)}px` }}
                    className="w-full bg-[#fde047]"
                    title={`Medium: ${t.medium_count}`}
                  />
                </div>
                <div className="text-xs font-mono text-ink-muted font-medium">{t.timestamp_label}</div>
              </div>
            ))}
          </div>

          <div className="flex items-center justify-center gap-6 mt-6 pt-4 border-t border-border text-xs text-ink-muted">
            <span className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 bg-status-critical rounded-sm" />
              Critical Risk
            </span>
            <span className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 bg-accent rounded-sm" />
              High Risk
            </span>
            <span className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 bg-[#fde047] rounded-sm" />
              Medium Risk
            </span>
          </div>
        </div>

        {/* Two Column Grid: Alerts Queue & Recent Transactions */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Active Alerts Queue */}
          <div className="p-6 bg-white border border-[#e2e8f0] rounded-lg flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-sm font-semibold text-ink">Active Alert Surveillance Queue</h2>
                <Link href="/alerts" className="text-xs text-accent hover:underline flex items-center gap-1 font-medium">
                  View All Alerts <ArrowRight className="w-3 h-3" />
                </Link>
              </div>

              <div className="space-y-3">
                {alerts.map((alert) => (
                  <div key={alert.id} className="p-3.5 bg-[#fbfaf8] border border-border rounded-md space-y-2">
                    <div className="flex items-start justify-between">
                      <div>
                        <div className="text-xs font-semibold text-ink">{alert.trigger_reason}</div>
                        <div className="text-[11px] font-mono text-ink-muted mt-0.5">
                          Tx: {alert.transaction_id} • Account: {alert.account_id}
                        </div>
                      </div>
                      <RiskBadge level={alert.risk_level} score={alert.risk_score} />
                    </div>

                    <div className="flex items-center justify-between text-xs pt-1 border-t border-border/50">
                      <span className="font-mono font-medium text-ink">
                        {alert.transaction_amount ? formatCurrency(alert.transaction_amount, alert.transaction_currency) : "—"}
                      </span>
                      <Link
                        href="/investigations"
                        className="text-accent hover:underline font-medium text-xs flex items-center gap-1"
                      >
                        Investigate Case <ArrowUpRight className="w-3 h-3" />
                      </Link>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Recent Ingested Transactions */}
          <div className="p-6 bg-white border border-[#e2e8f0] rounded-lg flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-sm font-semibold text-ink">Recent Ingested Transactions</h2>
                <Link href="/transactions" className="text-xs text-accent hover:underline flex items-center gap-1 font-medium">
                  View Transactions <ArrowRight className="w-3 h-3" />
                </Link>
              </div>

              <div className="divide-y divide-border">
                {transactions.slice(0, 5).map((tx) => (
                  <div key={tx.id} className="py-2.5 flex items-center justify-between text-xs">
                    <div>
                      <div className="font-mono font-semibold text-ink">{tx.transaction_id}</div>
                      <div className="text-[11px] text-ink-muted">
                        {tx.transaction_type.toUpperCase()} • {tx.channel} • {formatDate(tx.timestamp)}
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="font-mono font-semibold text-ink">
                        {formatCurrency(tx.amount, tx.currency)}
                      </div>
                      <div className="mt-0.5">
                        <RiskBadge level={tx.risk_level || "low"} score={tx.risk_score} />
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
