"use client";

import React from "react";
import Link from "next/link";
import { SignUp } from "@clerk/nextjs";
import { Shield, Lock, CheckCircle2, FileText, ArrowRight } from "lucide-react";

export default function SignUpPage() {
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
              Create Analyst Account
            </h1>
            <p className="mt-3 text-sm text-slate-400 leading-relaxed">
              Register authorized security credentials to access FinGuard AI fraud detection, risk triage queues, and forensic AI investigation tools.
            </p>
          </div>

          <div className="space-y-4">
            <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 flex items-start gap-3.5">
              <div className="w-8 h-8 rounded-lg bg-blue-950 border border-blue-800 flex items-center justify-center shrink-0 mt-0.5">
                <Lock className="w-4 h-4 text-blue-400" />
              </div>
              <div>
                <h2 className="text-xs font-semibold text-slate-200 uppercase tracking-wide">
                  Enterprise-Grade Access Control
                </h2>
                <p className="text-xs text-slate-400 mt-0.5">
                  Role-based permissions and session token security powered by Clerk.
                </p>
              </div>
            </div>

            <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 flex items-start gap-3.5">
              <div className="w-8 h-8 rounded-lg bg-indigo-950 border border-indigo-800 flex items-center justify-center shrink-0 mt-0.5">
                <CheckCircle2 className="w-4 h-4 text-indigo-400" />
              </div>
              <div>
                <h2 className="text-xs font-semibold text-slate-200 uppercase tracking-wide">
                  Active Human-In-The-Loop Clearance
                </h2>
                <p className="text-xs text-slate-400 mt-0.5">
                  Take conclusive triage actions: Clear false positives, Escalate to leads, or Confirm fraud.
                </p>
              </div>
            </div>

            <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 flex items-start gap-3.5">
              <div className="w-8 h-8 rounded-lg bg-emerald-950 border border-emerald-800 flex items-center justify-center shrink-0 mt-0.5">
                <FileText className="w-4 h-4 text-emerald-400" />
              </div>
              <div>
                <h2 className="text-xs font-semibold text-slate-200 uppercase tracking-wide">
                  Forensic Audit Trail
                </h2>
                <p className="text-xs text-slate-400 mt-0.5">
                  All case interventions are recorded in the PostgreSQL immutable audit log with cryptographic timestamps.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Trust & Verification Note */}
        <div className="relative z-10 pt-6 border-t border-slate-800/80 flex items-center justify-between text-xs text-slate-500">
          <span>SOC-2 & ISO 27001 Alignment</span>
          <Link href="/sign-in" className="text-blue-400 hover:text-blue-300 font-medium inline-flex items-center gap-1">
            Already have an account? Sign In <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      </div>

      {/* Right Custom Registration Console */}
      <div className="lg:w-1/2 flex items-center justify-center p-6 sm:p-12 relative bg-[#fbfaf8]">
        <div className="w-full max-w-md flex flex-col items-center">
          <div className="w-full mb-6 text-center lg:text-left">
            <h2 className="text-2xl font-semibold text-slate-900 tracking-tight">Analyst Registration</h2>
            <p className="text-xs text-slate-500 mt-1">
              Initialize your security profile to access the live financial surveillance dashboard.
            </p>
          </div>

          <div className="w-full flex justify-center">
            <SignUp
              routing="path"
              path="/sign-up"
              signInUrl="/sign-in"
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
            <span>Already registered? </span>
            <Link href="/sign-in" className="text-blue-600 hover:underline font-medium">
              Sign In to existing workspace
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
