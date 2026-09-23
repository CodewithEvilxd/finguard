import React from "react";
import { AppHeader } from "@/components/AppHeader";
import { RiskBadge } from "@/components/RiskBadge";
import { api } from "@/services/api";
import { formatCurrency, formatDate } from "@/lib/utils";
import { ArrowLeftRight, Download, Filter, Plus } from "lucide-react";

export default async function TransactionsPage() {
  const { items: transactions = [] } = await api.getTransactions();

  return (
    <div className="flex-1 flex flex-col">
      <AppHeader
        title="Transaction Intelligence"
        subtitle="Real-time multi-channel ingestion, validation, and surveillance feed"
      />

      <main className="p-8 space-y-6 max-w-7xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold text-ink uppercase tracking-wider">Channel Filter:</span>
            <span className="px-2.5 py-1 bg-navy text-white text-xs font-medium rounded-md">All ({transactions.length})</span>
            <span className="px-2.5 py-1 bg-white border border-border text-ink-muted text-xs font-medium rounded-md hover:text-ink cursor-pointer">
              Wires
            </span>
            <span className="px-2.5 py-1 bg-white border border-border text-ink-muted text-xs font-medium rounded-md hover:text-ink cursor-pointer">
              Purchases
            </span>
            <span className="px-2.5 py-1 bg-white border border-border text-ink-muted text-xs font-medium rounded-md hover:text-ink cursor-pointer">
              Transfers
            </span>
          </div>

          <div className="flex items-center gap-2">
            <button
              type="button"
              className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-white border border-border rounded-md text-xs font-medium text-ink hover:bg-[#f4f2ee]"
            >
              <Download className="w-3.5 h-3.5" />
              Export CSV
            </button>
            <button
              type="button"
              className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-accent text-white rounded-md text-xs font-medium hover:bg-accent-hover shadow-sm"
            >
              <Plus className="w-3.5 h-3.5" />
              Simulate Ingestion
            </button>
          </div>
        </div>

        {/* Transactions Table */}
        <div className="bg-white border border-[#e2e8f0] rounded-lg overflow-hidden shadow-sm">
          <table className="w-full text-left text-xs">
            <thead className="bg-[#f4f2ee] border-b border-[#e2e8f0] text-ink-muted uppercase tracking-wider font-semibold">
              <tr>
                <th className="py-3 px-4">Transaction ID</th>
                <th className="py-3 px-4">Account ID</th>
                <th className="py-3 px-4">Timestamp</th>
                <th className="py-3 px-4">Type</th>
                <th className="py-3 px-4">Channel</th>
                <th className="py-3 px-4 text-right">Amount</th>
                <th className="py-3 px-4 text-center">Status</th>
                <th className="py-3 px-4 text-right">Risk Score</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {transactions.map((tx) => (
                <tr key={tx.id} className="hover:bg-[#fbfaf8] transition-colors">
                  <td className="py-3 px-4 font-mono font-semibold text-ink">{tx.transaction_id}</td>
                  <td className="py-3 px-4 font-mono text-ink-muted">{tx.account_id}</td>
                  <td className="py-3 px-4 text-ink-muted">{formatDate(tx.timestamp)}</td>
                  <td className="py-3 px-4 capitalize text-ink">{tx.transaction_type}</td>
                  <td className="py-3 px-4 capitalize text-ink-muted">{tx.channel}</td>
                  <td className="py-3 px-4 font-mono font-semibold text-ink text-right">
                    {formatCurrency(tx.amount, tx.currency)}
                  </td>
                  <td className="py-3 px-4 text-center">
                    <span
                      className={`inline-block px-2 py-0.5 rounded text-[11px] font-medium uppercase tracking-wider ${
                        tx.status === "flagged"
                          ? "bg-accent-light text-accent border border-accent-border"
                          : "bg-slate-100 text-slate-700"
                      }`}
                    >
                      {tx.status}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-right">
                    <RiskBadge level={tx.risk_level || "low"} score={tx.risk_score} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  );
}
