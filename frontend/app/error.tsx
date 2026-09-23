"use client";

import React, { useEffect } from "react";
import Link from "next/link";
import { AlertCircle, RotateCcw } from "lucide-react";

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error("FinGuard Runtime Exception:", error);
  }, [error]);

  return (
    <div className="min-h-screen bg-[#fbfaf8] flex flex-col items-center justify-center p-6 text-center">
      <div className="w-12 h-12 rounded-full bg-red-100 flex items-center justify-center text-red-600 mb-4">
        <AlertCircle className="w-6 h-6" />
      </div>
      <h2 className="text-xl font-semibold text-slate-900 tracking-tight">Security System Exception</h2>
      <p className="text-xs text-slate-500 mt-2 max-w-md">
        An unexpected runtime exception was captured. Session security parameters remain isolated.
      </p>
      <div className="mt-6 flex items-center gap-3">
        <button
          onClick={() => reset()}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-md bg-[#0f172a] text-white text-xs font-semibold hover:bg-slate-800 transition-colors shadow-sm"
        >
          <RotateCcw className="w-3.5 h-3.5" /> Retry Request
        </button>
        <Link
          href="/"
          className="px-4 py-2 rounded-md border border-slate-300 text-xs font-semibold text-slate-700 hover:bg-slate-100 transition-colors"
        >
          Return Home
        </Link>
      </div>
    </div>
  );
}
