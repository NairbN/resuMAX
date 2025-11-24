import type { ReactNode } from "react";
import { cn } from "@/lib/utils";

type ContainerProps = {
  children: ReactNode;
  className?: string;
};

export function Container({ children, className }: ContainerProps) {
  return (
    <main
      className={cn(
        "mx-auto flex min-h-screen max-w-5xl flex-col px-6 py-12 md:px-10 md:py-16",
        className,
      )}
    >
      {children}
    </main>
  );
}
