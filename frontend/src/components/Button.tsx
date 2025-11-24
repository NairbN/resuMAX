import Link from "next/link";
import type { AnchorHTMLAttributes, ButtonHTMLAttributes, ReactNode } from "react";
import { cn } from "@/lib/utils";

type Variant = "primary" | "secondary" | "ghost";
type Size = "md" | "lg";

type ButtonBaseProps = {
  children: ReactNode;
  className?: string;
  variant?: Variant;
  size?: Size;
};

type ButtonAsButton = ButtonBaseProps &
  ButtonHTMLAttributes<HTMLButtonElement> & {
    href?: undefined;
  };

type ButtonAsLink = ButtonBaseProps &
  AnchorHTMLAttributes<HTMLAnchorElement> & {
    href: string;
  };

export type ButtonProps = ButtonAsButton | ButtonAsLink;

const variantClasses: Record<Variant, string> = {
  primary: "bg-emerald-400 text-slate-950 hover:bg-emerald-300",
  secondary:
    "border border-white/20 text-white hover:border-emerald-300/70 hover:text-emerald-50",
  ghost: "text-white hover:text-emerald-50 hover:bg-white/5",
};

const sizeClasses: Record<Size, string> = {
  md: "px-5 py-3 text-base",
  lg: "px-6 py-3.5 text-lg",
};

const baseClasses =
  "inline-flex items-center justify-center gap-2 rounded-full font-semibold transition will-change-transform hover:translate-y-0.5 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-300 disabled:pointer-events-none disabled:opacity-60";

export function Button(props: ButtonProps) {
  const { children, className, variant = "primary", size = "md", ...rest } = props;
  const composed = cn(baseClasses, variantClasses[variant], sizeClasses[size], className);

  if ("href" in rest && rest.href) {
    const { href, ...linkProps } = rest;
    return (
      <Link href={href} className={composed} {...linkProps}>
        {children}
      </Link>
    );
  }

  return (
    <button className={composed} {...rest}>
      {children}
    </button>
  );
}
