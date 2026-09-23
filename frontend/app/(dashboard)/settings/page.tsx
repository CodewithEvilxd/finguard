import React from "react";
import { AppHeader } from "@/components/AppHeader";
import { Sliders, Save, Shield } from "lucide-react";

export default function SettingsPage() {
  return (
    <div className="flex-1 flex flex-col">
      <AppHeader
        title="Rules & Scoring Settings"
        subtitle="Configurable multi-tier risk weights, policy triggers, and alert notification thresholds"
      />

      <main className="p-8 space-y-6 max-w-4xl">
        <div className="p-6 bg-white border border-[#e2e8f0] rounded-lg space-y-6">
          <div>
            <h3 className="text-sm font-semibold text-ink">Unified Risk Engine Component Weights</h3>
            <p className="text-xs text-ink-muted mt-0.5">
              Adjust relative contributions for the final unified risk calculation. Weights normalize automatically.
            </p>
          </div>

          <div className="space-y-4 text-xs">
            <div>
              <div className="flex justify-between font-medium text-ink mb-1.5">
                <span>Supervised Classifier (XGBoost)</span>
                <span className="font-mono text-accent">0.45</span>
              </div>
              <input type="range" min="0" max="1" step="0.05" defaultValue="0.45" className="w-full accent-accent" />
            </div>

            <div>
              <div className="flex justify-between font-medium text-ink mb-1.5">
                <span>Unsupervised Anomaly (Isolation Forest)</span>
                <span className="font-mono text-accent">0.25</span>
              </div>
              <input type="range" min="0" max="1" step="0.05" defaultValue="0.25" className="w-full accent-accent" />
            </div>

            <div>
              <div className="flex justify-between font-medium text-ink mb-1.5">
                <span>Deterministic Business Risk Rules</span>
                <span className="font-mono text-accent">0.30</span>
              </div>
              <input type="range" min="0" max="1" step="0.05" defaultValue="0.30" className="w-full accent-accent" />
            </div>
          </div>

          <div className="pt-4 border-t border-border">
            <h3 className="text-sm font-semibold text-ink mb-2">Alert Generation Cutoffs</h3>
            <div className="grid grid-cols-3 gap-4 text-xs">
              <div className="p-3 bg-[#fbfaf8] border border-border rounded">
                <div className="font-semibold text-ink">Medium Alert Threshold</div>
                <div className="font-mono text-status-medium text-sm mt-1">Score ≥ 35.0</div>
              </div>
              <div className="p-3 bg-[#fbfaf8] border border-border rounded">
                <div className="font-semibold text-ink">High Alert Threshold</div>
                <div className="font-mono text-accent text-sm mt-1">Score ≥ 65.0</div>
              </div>
              <div className="p-3 bg-[#fbfaf8] border border-border rounded">
                <div className="font-semibold text-ink">Critical Alert Threshold</div>
                <div className="font-mono text-status-critical text-sm mt-1">Score ≥ 85.0</div>
              </div>
            </div>
          </div>

          <div className="pt-2 flex justify-end">
            <button
              type="button"
              className="inline-flex items-center gap-1.5 px-4 py-2 bg-navy text-white text-xs font-semibold rounded-md hover:bg-navy-dark transition-colors"
            >
              <Save className="w-3.5 h-3.5" />
              Save Configuration
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}
