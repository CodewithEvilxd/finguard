"use client";

import React from "react";
import { Bell, Search, ShieldCheck } from "lucide-react";
import { UserButton, Show } from "@clerk/nextjs";
import Link from "next/link";

interface AppHeaderProps {
  title: string;
  subtitle?: string;
}

export const AppHeader: React.FC<AppHeaderProps> = ({ title, subtitle }) => {
  return (
    <header className="h-16 bg-[#fbfaf8] border-b border-[#e2e8f0] px-8 flex items-center justify-between sticky top-0 z-40">
      <div>
        <h1 className="text-lg font-semibold text-ink tracking-tight">{title}</h1>
        {subtitle && <p className="text-xs text-ink-muted">{subtitle}</p>}
      </div>

      <div className="flex items-center gap-4">
        {/* Environment Badge */}
        <div className="hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded bg-[#f4f2ee] border border-border text-xs text-ink-muted">
          <ShieldCheck className="w-3.5 h-3.5 text-status-low" />
          <span>Production Sentinel</span>
        </div>

        {/* Search Input Placeholder */}
        <div className="relative hidden md:block">
          <Search className="w-3.5 h-3.5 text-ink-faint absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search transactions, accounts..."
            className="w-64 pl-8 pr-3 py-1.5 text-xs bg-[#f4f2ee] border border-border rounded-md focus:outline-none focus:border-accent text-ink placeholder:text-ink-faint"
          />
        </div>

        {/* Notifications */}
        <button
          type="button"
          aria-label="Alert notifications"
          className="relative p-2 text-ink-muted hover:text-ink hover:bg-[#f4f2ee] rounded-md transition-colors"
        >
          <Bell className="w-4 h-4" />
          <span className="w-2 h-2 bg-accent rounded-full absolute top-1.5 right-1.5" />
        </button>

        {/* Analyst Profile - Clerk Live Auth */}
        <div className="flex items-center gap-2.5 pl-3 border-l border-border">
          <Show when="signed-in">
            <div className="flex items-center gap-2">
              <UserButton
                appearance={{
                  elements: {
                    avatarBox: "w-8 h-8 border border-border shadow-sm",
                  },
                }}
              />
              <div className="hidden lg:block text-left">
                <div className="text-xs font-semibold text-ink">Active Analyst</div>
                <div className="text-[10px] text-ink-muted font-mono">Verified Session</div>
              </div>
            </div>
          </Show>

          <Show when="signed-out">
            <Link
              href="/sign-in"
              className="px-3 py-1.5 text-xs font-semibold rounded bg-navy text-white hover:bg-navy-dark transition-colors"
            >
              Sign In
            </Link>
          </Show>
        </div>
      </div>
    </header>
  );
};
