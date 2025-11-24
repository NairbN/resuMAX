import type { ReactNode } from "react";
import { Card } from "@/components/Card";

type AuthCardProps = {
  children: ReactNode;
  accent?: boolean;
};

export function AuthCard({ children, accent = false }: AuthCardProps) {
  return <Card tone={accent ? "accent" : "neutral"}>{children}</Card>;
}
