import type { ReactNode } from "react";
import { Container } from "@/components/Container";
import { Pill } from "@/components/Pill";
import { SectionHeader } from "@/components/SectionHeader";

type AuthShellProps = {
  title: string;
  description: string;
  pillLabel?: string;
  pillText?: string;
  children: ReactNode;
};

export function AuthShell({
  title,
  description,
  pillLabel = "resuMAX",
  pillText,
  children,
}: AuthShellProps) {
  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <Container className="justify-center">
        <div className="w-full max-w-xl space-y-8">
          <Pill>
            <span className="font-medium text-emerald-300">{pillLabel}</span>
            {pillText ? <span className="text-white/80">{pillText}</span> : null}
          </Pill>

          <SectionHeader title={title} description={description} />

          {children}
        </div>
      </Container>
    </div>
  );
}
