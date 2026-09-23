import React from "react";
import { RiskLevel } from "@/types";
import { cn } from "@/lib/utils";

interface RiskBadgeProps {
  level: RiskLevel | string;
  score?: number | null;
  className?: string;
}

export const RiskBadge: React.FC<RiskBadgeProps> = ({ level, score, className }) => {
  const normLevel = (level || "low").toLowerCase();

  const styles = {
    low: "bg-status-lowBg text-status-low border-status-lowBorder",
    medium: "bg-status-mediumBg text-status-medium border-status-mediumBorder",
    high: "bg-status-highBg text-status-high border-status-highBorder",
    critical: "bg-status-criticalBg text-status-critical border-status-criticalBorder",
  }[normLevel] || "bg-slate-100 text-slate-800 border-slate-300";

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium border uppercase tracking-wider",
        styles,
        className
      )}
    >
      <span className="w-1.5 h-1.5 rounded-full bg-current" />
      {normLevel}
      {score !== undefined && score !== null && (
        <span className="font-mono font-semibold ml-0.5">({score.toFixed(0)})</span>
      )}
    </span>
  );
};
