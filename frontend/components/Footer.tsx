import React from "react";
import Link from "next/link";
import { Shield } from "lucide-react";

export const Footer: React.FC = () => {
  return (
    <footer className="w-full bg-[#f4f2ee] border-t border-[#e2e8f0] py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          <div className="col-span-1 md:col-span-1">
            <div className="flex items-center gap-2 mb-3">
              <div className="w-6 h-6 rounded bg-navy flex items-center justify-center text-white">
                <Shield className="w-3.5 h-3.5 text-white" />
              </div>
              <span className="font-semibold text-ink text-base">FinGuard AI</span>
            </div>
            <p className="text-xs text-ink-muted leading-relaxed">
              Explainable financial intelligence platform combining XGBoost fraud classification, Isolation Forest anomaly scoring, and grounded AI investigation.
            </p>
          </div>

          <div>
            <h4 className="text-xs font-semibold text-ink uppercase tracking-wider mb-3">Detection Stack</h4>
            <ul className="space-y-2 text-xs text-ink-muted">
              <li>Supervised Fraud Classifier</li>
              <li>Unsupervised Anomaly Scoring</li>
              <li>Deterministic Rule Engine</li>
              <li>SHAP Force Explainability</li>
            </ul>
          </div>

          <div>
            <h4 className="text-xs font-semibold text-ink uppercase tracking-wider mb-3">Investigation & RAG</h4>
            <ul className="space-y-2 text-xs text-ink-muted">
              <li>pgvector Document Indexing</li>
              <li>Grounded Policy Retrieval</li>
              <li>Evidence-Based Summaries</li>
              <li>Immutable Audit Trails</li>
            </ul>
          </div>

          <div>
            <h4 className="text-xs font-semibold text-ink uppercase tracking-wider mb-3">Platform Access</h4>
            <ul className="space-y-2 text-xs text-ink-muted">
              <li>
                <Link href="/demo" className="hover:text-ink transition-colors">
                  Interactive Demo Sandbox
                </Link>
              </li>
              <li>
                <Link href="/dashboard" className="hover:text-ink transition-colors">
                  Operational Dashboard
                </Link>
              </li>
              <li>
                <Link href="/login" className="hover:text-ink transition-colors">
                  Analyst Sign In
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <div className="pt-8 border-t border-border flex flex-col sm:flex-row items-center justify-between text-xs text-ink-faint">
          <p>© 2026 FinGuard AI. Designed for human-in-the-loop financial compliance.</p>
          <p className="mt-2 sm:mt-0 font-mono">System Status: Operational • Surveillance Active</p>
        </div>
      </div>
    </footer>
  );
};
