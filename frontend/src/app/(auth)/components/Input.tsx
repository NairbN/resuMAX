import type { InputHTMLAttributes } from "react";
import { cn } from "@/lib/utils";

export type InputProps = InputHTMLAttributes<HTMLInputElement>;

const baseClasses =
  "w-full rounded-xl border border-white/12 bg-white/5 px-4 py-3 text-white placeholder:text-white/50 focus:border-emerald-300 focus:outline-none focus:ring-2 focus:ring-emerald-300/30";

export function Input({ className, ...rest }: InputProps) {
  return <input className={cn(baseClasses, className)} {...rest} />;
}
