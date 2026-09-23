"use client";

import React from "react";
import Link from "next/link";
import { SignIn } from "@clerk/nextjs";
import { Shield, Cpu, Sparkles, FileCheck, ArrowRight } from "lucide-react";

export default function SignInPage() {
  return (
    <div className="min-h-screen bg-[#fbfaf8] flex flex-col lg:flex-row">
      {/* Left Intelligence & Security Panel */}
      <div className="lg:w-1/2 bg-[#0f172a] text-white p-8 lg:p-16 flex flex-col justify-between relative overflow-hidden border-r border-[#1e293b]">
        {/* Subtle Background Glow */}
        <div className="absolute -top-32 -left-32 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute -bottom-32 -right-32 w-96 h-96 bg-indigo-600/10 rounded-full blur-3xl pointer-events-none" />

        {/* Top Brand Link */}
        <div className="relative z-10">
          <Link href="/" className="inline-flex items-center gap-2.5 group">
            <div className="w-9 h-9 rounded-lg bg-blue-600 flex items-center justify-center text-white shadow-md shadow-blue-500/20">
              <Shield className="w-5 h-5 text-white" />
            </div>
            <div>
              <span className="font-semibold text-white tracking-tight text-xl">FinGuard AI</span>
              <span className="text-[10px] font-mono tracking-widest text-blue-400 uppercase border border-blue-500/30 bg-blue-950/60 px-1.5 py-0.5 rounded ml-2">
                Enterprise Console
              </span>
            </div>
          </Link>
        </div>

        {/* Central Platform Highlights */}
        <div className="my-12 relative z-10 space-y-8 max-w-lg">
          <div>
            <h1 className="text-3xl lg:text-4xl font-semibold tracking-tight text-white leading-tight">
              Enterprise Financial Fraud & Anomaly Intelligence
            </h1>
            <p className="mt-3 text-sm text-slate-400 leading-relaxed">
              Log in to the secure analyst surveillance console. Real-time transaction validation, TreeSHAP explainability, and multi-tier fraud scoring.
            </p>
          </div>

          <div className="space-y-4">
            <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 flex items-start gap-3.5">
              <div className="w-8 h-8 rounded-lg bg-blue-950 border border-blue-800 flex items-center justify-center shrink-0 mt-0.5">
                <Cpu className="w-4 h-4 text-blue-400" />
              </div>
              <div>
                <h2 className="text-xs font-semibold text-slate-200 uppercase tracking-wide">
                  Dual ML Intelligence Triad
                </h2>
                <p className="text-xs text-slate-400 mt-0.5">
                  XGBoost supervised classification coupled with Isolation Forest unsupervised anomaly detection.
                </p>
              </div>
            </div>

            <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 flex items-start gap-3.5">
              <div className="w-8 h-8 rounded-lg bg-indigo-950 border border-indigo-800 flex items-center justify-center shrink-0 mt-0.5">
                <Sparkles className="w-4 h-4 text-indigo-400" />
              </div>
              <div>
                <h2 className="text-xs font-semibold text-slate-200 uppercase tracking-wide">
                  Explainable TreeSHAP Reasoning
                </h2>
                <p className="text-xs text-slate-400 mt-0.5">
                  Every flagged score provides exact contributing factors and percentage attributions.
                </p>
              </div>
            </div>

            <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 flex items-start gap-3.5">
              <div className="w-8 h-8 rounded-lg bg-emerald-950 border border-emerald-800 flex items-center justify-center shrink-0 mt-0.5">
                <FileCheck className="w-4 h-4 text-emerald-400" />
              </div>
              <div>
                <h2 className="text-xs font-semibold text-slate-200 uppercase tracking-wide">
                  Regulatory & Audit Integrity
                </h2>
                <p className="text-xs text-slate-400 mt-0.5">
                  Immutable audit trail logging analyst sign-offs, case triage, and automated security triggers.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Trust & Verification Note */}
        <div className="relative z-10 pt-6 border-t border-slate-800/80 flex items-center justify-between text-xs text-slate-500">
          <span>Encrypted Session Management</span>
          <Link href="/demo" className="text-blue-400 hover:text-blue-300 font-medium inline-flex items-center gap-1">
            Access Live Interactive Demo <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      </div>

      {/* Right Custom Authentication Console */}
      <div className="lg:w-1/2 flex items-center justify-center p-6 sm:p-12 relative bg-[#fbfaf8]">
        <div className="w-full max-w-md flex flex-col items-center">
          <div className="w-full mb-6 text-center lg:text-left">
            <h2 className="text-2xl font-semibold text-slate-900 tracking-tight">Analyst Sign In</h2>
            <p className="text-xs text-slate-500 mt-1">
              Authenticate with your enterprise credentials to access active surveillance and investigation dossiers.
            </p>
          </div>

          <div className="w-full flex justify-center">
            <SignIn
              routing="path"
              path="/sign-in"
              signUpUrl="/sign-up"
              forceRedirectUrl="/dashboard"
              appearance={{
                elements: {
                  rootBox: "w-full",
                  card: "w-full shadow-sm border border-slate-200 rounded-xl bg-white p-6",
                  headerTitle: "hidden",
                  headerSubtitle: "hidden",
                  formButtonPrimary:
                    "bg-[#0f172a] hover:bg-slate-800 text-white font-medium text-xs py-2.5 transition-colors shadow-sm",
                  formFieldInput:
                    "bg-slate-50 border-slate-300 text-xs text-slate-900 focus:border-blue-600 focus:ring-1 focus:ring-blue-600 rounded-lg",
                  formFieldLabel: "text-xs font-medium text-slate-700",
                  footerActionLink: "text-blue-600 hover:text-blue-700 font-medium text-xs",
                  identityPreviewText: "text-xs text-slate-600",
                  identityPreviewEditButton: "text-xs text-blue-600",
                },
              }}
            />
          </div>

          <div className="mt-6 text-center text-xs text-slate-500">
            <span>Looking for immediate walkthrough? </span>
            <Link href="/demo" className="text-blue-600 hover:underline font-medium">
              Launch Sandbox Mode
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
