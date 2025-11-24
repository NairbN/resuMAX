import type { ReactNode } from "react";
import { cn } from "@/lib/utils";

type SectionHeaderProps = {
  eyebrow?: ReactNode;
  title: ReactNode;
  description?: ReactNode;
  className?: string;
};

export function SectionHeader({ eyebrow, title, description, className }: SectionHeaderProps) {
  return (
    <div className={cn("flex flex-col gap-3", className)}>
      {eyebrow ? <div className="text-sm font-semibold text-emerald-300">{eyebrow}</div> : null}
      <h1 className="text-4xl font-semibold leading-tight tracking-tight sm:text-5xl">{title}</h1>
      {description ? <p className="max-w-2xl text-lg text-white/80">{description}</p> : null}
    </div>
  );
}
