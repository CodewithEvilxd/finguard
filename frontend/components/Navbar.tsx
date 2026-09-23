"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import {
  Shield,
  Search,
  Sparkles,
  ArrowRight,
  LayoutDashboard,
  X,
  Command,
  Activity,
  Layers,
  Cpu,
  Menu,
} from "lucide-react";
import { Show, UserButton } from "@clerk/nextjs";

export const Navbar: React.FC = () => {
  const [scrolled, setScrolled] = useState(false);
  const [spotlightOpen, setSpotlightOpen] = useState(false);
  const [spotlightQuery, setSpotlightQuery] = useState("");
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Dynamic elevation on scroll
  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 10);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  // Global Keyboard Shortcut (⌘K / Ctrl+K)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setSpotlightOpen((prev) => !prev);
      } else if (e.key === "Escape") {
        setSpotlightOpen(false);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  const searchResults = [
    { title: "Live Pipeline Demo", desc: "Interactive 4-stage surveillance runbook", href: "/demo", icon: Sparkles },
    { title: "Analyst Risk Console", desc: "Transactions, alerts, investigations dashboard", href: "/dashboard", icon: LayoutDashboard },
    { title: "Platform Capabilities", desc: "Multi-modal detection and TreeSHAP explainability", href: "/#capabilities", icon: Activity },
    { title: "System Architecture", desc: "Pipeline, Cloud & Vector RAG topologies", href: "/#architecture", icon: Layers },
    { title: "Explainable Intelligence", desc: "NIST explainability principles & comparison", href: "/#explainability", icon: Cpu },
    { title: "Analyst Sign In", desc: "Authentication and role management console", href: "/sign-in", icon: Shield },
  ].filter(
    (item) =>
      item.title.toLowerCase().includes(spotlightQuery.toLowerCase()) ||
      item.desc.toLowerCase().includes(spotlightQuery.toLowerCase())
  );

  return (
    <>
      {/* World-Class Apple-Grade Frosted Glass Sticky Navbar */}
      <header
        className={`sticky top-0 left-0 right-0 z-50 w-full transition-all duration-200 ${
          scrolled
            ? "bg-white/85 backdrop-blur-xl border-b border-slate-200/80 shadow-[0_2px_12px_rgba(0,0,0,0.03)]"
            : "bg-white/70 backdrop-blur-md border-b border-slate-200/50"
        }`}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          {/* Brand Mark & Title */}
          <div className="flex items-center gap-6">
            <Link href="/" className="flex items-center gap-2.5 group">
              <div className="w-8 h-8 rounded-lg bg-slate-900 text-white flex items-center justify-center shadow-xs group-hover:bg-slate-800 transition-colors">
                <Shield className="w-4 h-4 fill-white text-white" />
              </div>
              <div className="flex items-center gap-2">
                <span className="font-semibold text-slate-900 tracking-tight text-base">
                  FinGuard
                </span>
                <span className="text-[10px] font-mono tracking-wider font-semibold text-slate-500 bg-slate-100 border border-slate-200/80 px-1.5 py-0.5 rounded">
                  AI
                </span>
              </div>
            </Link>
          </div>

          {/* Navigation Links */}
          <nav className="hidden md:flex items-center gap-1">
            <Link
              href="/#capabilities"
              className="px-3.5 py-1.5 text-xs font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-100/70 rounded-full transition-all duration-150"
            >
              Capabilities
            </Link>
            <Link
              href="/#architecture"
              className="px-3.5 py-1.5 text-xs font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-100/70 rounded-full transition-all duration-150"
            >
              Architecture
            </Link>
            <Link
              href="/#explainability"
              className="px-3.5 py-1.5 text-xs font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-100/70 rounded-full transition-all duration-150"
            >
              Explainability
            </Link>
            <Link
              href="/#governance"
              className="px-3.5 py-1.5 text-xs font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-100/70 rounded-full transition-all duration-150"
            >
              Governance
            </Link>
            <Link
              href="/demo"
              className="px-3.5 py-1.5 text-xs font-medium text-slate-700 hover:text-slate-900 hover:bg-slate-100/70 rounded-full transition-all duration-150 flex items-center gap-1"
            >
              <span>Live Runbook</span>
              <span className="text-[9px] font-mono uppercase bg-slate-100 border border-slate-200/80 px-1 py-0.2 rounded text-slate-600">
                Demo
              </span>
            </Link>
          </nav>

          {/* Right Controls: Quick Search, Auth & Action Button */}
          <div className="flex items-center gap-3">
            {/* Spotlight Search Trigger */}
            <button
              type="button"
              onClick={() => setSpotlightOpen(true)}
              className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-100/80 hover:bg-slate-100 border border-slate-200/70 text-xs text-slate-500 hover:text-slate-800 transition-colors"
              title="Search FinGuard (⌘K)"
            >
              <Search className="w-3.5 h-3.5 text-slate-400" />
              <span>Search</span>
              <kbd className="font-mono text-[10px] text-slate-400 bg-white border border-slate-200 px-1 py-0.2 rounded shadow-2xs">
                ⌘K
              </kbd>
            </button>

            {/* Signed-Out State */}
            <Show when="signed-out">
              <Link
                href="/sign-in"
                className="hidden sm:inline-flex text-xs font-medium text-slate-600 hover:text-slate-900 px-3 py-1.5 rounded-full hover:bg-slate-100/60 transition-colors"
              >
                Sign In
              </Link>
              <Link
                href="/demo"
                className="inline-flex items-center gap-1.5 px-4 py-2 rounded-full bg-slate-900 text-white text-xs font-medium hover:bg-slate-800 transition-all shadow-sm hover:scale-[1.02] active:scale-[0.98]"
              >
                <Sparkles className="w-3.5 h-3.5 text-white/90" />
                <span>Launch Demo</span>
                <ArrowRight className="w-3.5 h-3.5 opacity-80" />
              </Link>
            </Show>

            {/* Signed-In State */}
            <Show when="signed-in">
              <Link
                href="/dashboard"
                className="inline-flex items-center gap-1.5 px-4 py-2 rounded-full bg-slate-900 text-white text-xs font-medium hover:bg-slate-800 transition-all shadow-sm"
              >
                <LayoutDashboard className="w-3.5 h-3.5 text-white/90" />
                <span>Console</span>
              </Link>
              <div className="p-0.5 rounded-full border border-slate-200 shadow-2xs flex items-center justify-center">
                <UserButton
                  appearance={{
                    elements: {
                      avatarBox: "w-7 h-7",
                    },
                  }}
                />
              </div>
            </Show>

            {/* Mobile Hamburger Toggle */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              type="button"
              aria-label="Toggle navigation menu"
              className="p-2 rounded-full text-slate-600 hover:text-slate-900 hover:bg-slate-100 md:hidden transition-colors"
            >
              {mobileMenuOpen ? <X className="w-4 h-4" /> : <Menu className="w-4 h-4" />}
            </button>
          </div>
        </div>

        {/* Mobile Dropdown Panel */}
        {mobileMenuOpen && (
          <div className="border-t border-slate-200 bg-white/95 backdrop-blur-2xl px-4 py-4 md:hidden flex flex-col gap-2">
            <Link
              href="/#capabilities"
              onClick={() => setMobileMenuOpen(false)}
              className="px-3 py-2 text-xs font-medium text-slate-700 rounded-lg hover:bg-slate-100 transition-colors"
            >
              Capabilities
            </Link>
            <Link
              href="/#detection-flow"
              onClick={() => setMobileMenuOpen(false)}
              className="px-3 py-2 text-xs font-medium text-slate-700 rounded-lg hover:bg-slate-100 transition-colors"
            >
              Detection Flow
            </Link>
            <Link
              href="/#explainability"
              onClick={() => setMobileMenuOpen(false)}
              className="px-3 py-2 text-xs font-medium text-slate-700 rounded-lg hover:bg-slate-100 transition-colors"
            >
              Explainability
            </Link>
            <Link
              href="/#governance"
              onClick={() => setMobileMenuOpen(false)}
              className="px-3 py-2 text-xs font-medium text-slate-700 rounded-lg hover:bg-slate-100 transition-colors"
            >
              Governance
            </Link>
            <Link
              href="/demo"
              onClick={() => setMobileMenuOpen(false)}
              className="px-3 py-2 text-xs font-medium text-slate-700 rounded-lg hover:bg-slate-100 transition-colors"
            >
              Live Runbook Demo
            </Link>
            <div className="pt-3 border-t border-slate-200 flex items-center justify-between">
              <Show when="signed-out">
                <Link
                  href="/sign-in"
                  onClick={() => setMobileMenuOpen(false)}
                  className="text-xs font-medium text-slate-700 hover:text-slate-900"
                >
                  Sign In
                </Link>
                <Link
                  href="/demo"
                  onClick={() => setMobileMenuOpen(false)}
                  className="px-4 py-2 rounded-full bg-slate-900 text-white text-xs font-medium"
                >
                  Launch Demo
                </Link>
              </Show>
              <Show when="signed-in">
                <Link
                  href="/dashboard"
                  onClick={() => setMobileMenuOpen(false)}
                  className="text-xs font-medium text-slate-900 flex items-center gap-1.5"
                >
                  <LayoutDashboard className="w-3.5 h-3.5" />
                  Console Dashboard
                </Link>
              </Show>
            </div>
          </div>
        )}
      </header>

      {/* Apple-Style Spotlight Search Modal (⌘K) */}
      {spotlightOpen && (
        <div
          onClick={() => setSpotlightOpen(false)}
          className="fixed inset-0 z-50 flex items-start justify-center pt-24 px-4 bg-black/30 backdrop-blur-sm transition-all"
        >
          <div
            onClick={(e) => e.stopPropagation()}
            className="w-full max-w-lg rounded-2xl bg-white/95 backdrop-blur-2xl border border-slate-200/90 shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-150"
          >
            {/* Search Input Bar */}
            <div className="flex items-center gap-3 px-4 py-3.5 border-b border-slate-200/80">
              <Search className="w-4 h-4 text-slate-400 shrink-0" />
              <input
                type="text"
                autoFocus
                placeholder="Search FinGuard intelligence (demo, models, SHAP, console)..."
                value={spotlightQuery}
                onChange={(e) => setSpotlightQuery(e.target.value)}
                className="flex-1 bg-transparent text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none"
              />
              <button
                type="button"
                onClick={() => setSpotlightOpen(false)}
                className="p-1 rounded-md text-slate-400 hover:text-slate-600 transition-colors"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* Quick Result Items */}
            <div className="p-2 max-h-72 overflow-y-auto space-y-1">
              {searchResults.length > 0 ? (
                searchResults.map((item, idx) => (
                  <Link
                    key={idx}
                    href={item.href}
                    onClick={() => setSpotlightOpen(false)}
                    className="flex items-center justify-between p-2.5 rounded-xl hover:bg-slate-100 text-slate-800 transition-colors group"
                  >
                    <div className="flex items-center gap-3">
                      <div className="w-7 h-7 rounded-lg bg-slate-100 group-hover:bg-white flex items-center justify-center text-slate-600 transition-colors shadow-2xs">
                        <item.icon className="w-3.5 h-3.5" />
                      </div>
                      <div>
                        <div className="text-xs font-semibold text-slate-900">{item.title}</div>
                        <div className="text-[11px] text-slate-500">
                          {item.desc}
                        </div>
                      </div>
                    </div>
                    <ArrowRight className="w-3.5 h-3.5 text-slate-400 group-hover:text-slate-900 transition-colors" />
                  </Link>
                ))
              ) : (
                <div className="p-6 text-center text-xs text-slate-400">
                  No matching resources found for &ldquo;{spotlightQuery}&rdquo;
                </div>
              )}
            </div>

            {/* Footer Shortcut Helper */}
            <div className="px-4 py-2 bg-slate-50/80 border-t border-slate-200/80 flex items-center justify-between text-[11px] text-slate-400 font-mono">
              <span>ESC to exit</span>
              <span className="flex items-center gap-1">
                <Command className="w-3 h-3" />
                <span>+ K</span>
              </span>
            </div>
          </div>
        </div>
      )}
    </>
  );
};
