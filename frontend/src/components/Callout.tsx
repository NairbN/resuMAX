import type { ReactNode } from "react";
import { cn } from "@/lib/utils";

type CalloutProps = {
  title?: ReactNode;
  children: ReactNode;
  className?: string;
};

export function Callout({ title, children, className }: CalloutProps) {
  return (
    <div
      className={cn(
        "rounded-2xl border border-white/5 bg-white/5 px-6 py-5 text-sm text-white/80",
        className,
      )}
    >
      {title ? <p className="font-semibold text-white">{title}</p> : null}
      <div className={title ? "mt-2" : ""}>{children}</div>
    </div>
  );
}
