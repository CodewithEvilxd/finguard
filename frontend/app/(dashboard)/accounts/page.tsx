import React from "react";
import { AppHeader } from "@/components/AppHeader";
import { api } from "@/services/api";
import { formatCurrency } from "@/lib/utils";
import { ArrowUpRight, Building2, Shield } from "lucide-react";

export default async function AccountsPage() {
  const { items: fetchedAccounts = [] } = await api.getAccounts();

  const accounts = fetchedAccounts.length > 0 ? fetchedAccounts : [
    { id: "acc-1", account_number: "ACC-100482", account_holder: "Apex Global Logistics", balance: 245000.0, currency: "USD", risk_tier: "elevated", status: "active" },
    { id: "acc-2", account_number: "ACC-829104", account_holder: "Helios Semiconductor Corp", balance: 890000.0, currency: "USD", risk_tier: "standard", status: "active" },
    { id: "acc-3", account_number: "ACC-552019", account_holder: "Vanguard Retail Holdings", balance: 42000.0, currency: "USD", risk_tier: "high_risk", status: "active" },
    { id: "acc-4", account_number: "ACC-330192", account_holder: "Elena Rostova", balance: 18500.0, currency: "USD", risk_tier: "standard", status: "active" },
  ];

  return (
    <div className="flex-1 flex flex-col">
      <AppHeader
        title="Account Intelligence"
        subtitle="Surveillance across client accounts, counterparty entities, and historical volume profiles"
      />

      <main className="p-8 space-y-6 max-w-7xl">
        <div className="bg-white border border-[#e2e8f0] rounded-lg overflow-hidden shadow-sm">
          <table className="w-full text-left text-xs">
            <thead className="bg-[#f4f2ee] border-b border-[#e2e8f0] text-ink-muted uppercase tracking-wider font-semibold">
              <tr>
                <th className="py-3 px-4">Account Identifier</th>
                <th className="py-3 px-4">Accountholder Name</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4 text-right">Current Ledger Balance</th>
                <th className="py-3 px-4">Surveillance Tier</th>
                <th className="py-3 px-4 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {accounts.map((acc) => {
                const tier = acc.risk_tier.toLowerCase();
                const isHigh = tier.includes("high");
                const isElevated = tier.includes("elevated") || tier.includes("medium");
                return (
                  <tr key={acc.id} className="hover:bg-[#fbfaf8] transition-colors">
                    <td className="py-3 px-4 font-mono font-semibold text-ink">{acc.account_number}</td>
                    <td className="py-3 px-4 text-ink font-medium">{acc.account_holder}</td>
                    <td className="py-3 px-4 uppercase text-ink-muted text-[11px]">{acc.status}</td>
                    <td className="py-3 px-4 font-mono font-semibold text-ink text-right">
                      {formatCurrency(acc.balance, acc.currency)}
                    </td>
                    <td className="py-3 px-4">
                      <span
                        className={`inline-block px-2 py-0.5 rounded text-[11px] font-medium uppercase tracking-wider ${
                          isHigh
                            ? "bg-status-criticalBg text-status-critical border border-status-criticalBorder"
                            : isElevated
                            ? "bg-status-mediumBg text-status-medium border border-status-mediumBorder"
                            : "bg-status-lowBg text-status-low border border-status-lowBorder"
                        }`}
                      >
                        {acc.risk_tier}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right">
                      <button className="text-accent hover:underline font-medium inline-flex items-center gap-1">
                        Profile Dossier <ArrowUpRight className="w-3 h-3" />
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  );
}
