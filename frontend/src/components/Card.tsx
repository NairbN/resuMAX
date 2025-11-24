import type { ReactNode } from "react";
import { cn } from "@/lib/utils";

type CardTone = "neutral" | "muted" | "accent";

type CardProps = {
  children: ReactNode;
  tone?: CardTone;
  className?: string;
};

const toneClasses: Record<CardTone, string> = {
  neutral: "border-white/10 bg-white/5 shadow-2xl shadow-black/40",
  muted: "border-white/5 bg-white/5 shadow-xl shadow-black/30",
  accent: "border-emerald-300/25 bg-emerald-500/10 shadow-2xl shadow-black/40",
};

export function Card({ children, tone = "neutral", className }: CardProps) {
  return (
    <div className={cn("rounded-2xl p-8", toneClasses[tone], className)}>
      {children}
    </div>
  );
}
