import type { ReactNode } from "react";
import { Container } from "@/components/Container";

type DashboardShellProps = {
  children: ReactNode;
};

export function DashboardShell({ children }: DashboardShellProps) {
  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <Container className="min-h-screen space-y-10">
        {children}
      </Container>
    </div>
  );
}
