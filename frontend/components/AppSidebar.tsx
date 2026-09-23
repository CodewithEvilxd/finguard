"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  ArrowLeftRight,
  AlertTriangle,
  SearchCheck,
  Building2,
  LineChart,
  Settings,
  Shield,
  ExternalLink,
} from "lucide-react";
import { cn } from "@/lib/utils";

const navigationItems = [
  { name: "Overview", href: "/dashboard", icon: LayoutDashboard },
  { name: "Transactions", href: "/transactions", icon: ArrowLeftRight },
  { name: "Risk Alerts", href: "/alerts", icon: AlertTriangle, badge: "7" },
  { name: "Investigations", href: "/investigations", icon: SearchCheck, badge: "4" },
  { name: "Accounts", href: "/accounts", icon: Building2 },
  { name: "Analytics", href: "/analytics", icon: LineChart },
  { name: "Rules & Settings", href: "/settings", icon: Settings },
];

export const AppSidebar: React.FC = () => {
  const pathname = usePathname();

  return (
    <aside className="w-64 bg-[#fbfaf8] border-r border-[#e2e8f0] flex flex-col justify-between shrink-0 h-screen sticky top-0">
      <div>
        {/* Brand Header */}
        <div className="h-16 flex items-center px-6 border-b border-[#e2e8f0]">
          <Link href="/" className="flex items-center gap-2.5">
            <div className="w-7 h-7 rounded bg-navy flex items-center justify-center text-white">
              <Shield className="w-4 h-4 text-white" />
            </div>
            <span className="font-semibold text-ink tracking-tight text-base">FinGuard AI</span>
            <span className="text-[10px] font-mono tracking-widest text-accent uppercase border border-accent-border bg-accent-light px-1.5 py-0.5 rounded ml-1">
              Console
            </span>
          </Link>
        </div>

        {/* Navigation Menu */}
        <nav className="p-4 space-y-1">
          {navigationItems.map((item) => {
            const isActive = pathname === item.href || pathname?.startsWith(`${item.href}/`);
            return (
              <Link
                key={item.name}
                href={item.href}
                className={cn(
                  "flex items-center justify-between px-3 py-2 rounded-md text-sm font-medium transition-colors",
                  isActive
                    ? "bg-navy text-white"
                    : "text-ink-muted hover:bg-[#f4f2ee] hover:text-ink"
                )}
              >
                <div className="flex items-center gap-3">
                  <item.icon className={cn("w-4 h-4", isActive ? "text-white" : "text-ink-muted")} />
                  <span>{item.name}</span>
                </div>
                {item.badge && (
                  <span
                    className={cn(
                      "text-xs px-2 py-0.5 rounded-full font-mono font-semibold",
                      isActive
                        ? "bg-white/20 text-white"
                        : "bg-accent-light text-accent border border-accent-border"
                    )}
                  >
                    {item.badge}
                  </span>
                )}
              </Link>
            );
          })}
        </nav>
      </div>

      {/* Footer / System Status */}
      <div className="p-4 border-t border-[#e2e8f0] space-y-3">
        <div className="p-3 bg-[#f4f2ee] rounded-md text-xs space-y-1">
          <div className="flex items-center justify-between text-ink-muted font-medium">
            <span>Model Engine</span>
            <span className="text-status-low font-mono flex items-center gap-1">
              <span className="w-1.5 h-1.5 rounded-full bg-status-low" />
              Operational
            </span>
          </div>
          <div className="text-[11px] text-ink-faint">
            SHAP Attribution Active
          </div>
        </div>

        <Link
          href="/"
          className="flex items-center justify-between text-xs text-ink-muted hover:text-ink px-2 py-1 transition-colors"
        >
          <span>Back to Product Landing</span>
          <ExternalLink className="w-3.5 h-3.5" />
        </Link>
      </div>
    </aside>
  );
};
