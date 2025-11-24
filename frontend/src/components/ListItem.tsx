import type { ReactNode } from "react";
import { cn } from "@/lib/utils";

type ListItemProps = {
  children: ReactNode;
  className?: string;
};

export function ListItem({ children, className }: ListItemProps) {
  return (
    <li className={cn("flex items-start gap-2 text-sm text-white/80", className)}>
      <span className="mt-1 h-2 w-2 rounded-full bg-emerald-300" aria-hidden />
      <span>{children}</span>
    </li>
  );
}
