import type { ReactNode } from "react";
import { Card } from "@/components/Card";
import { Button } from "@/components/Button";
import { cn } from "@/lib/utils";

type StatCardProps = {
  title: string;
  subtitle?: string;
  actionLabel?: string;
  onActionClick?: () => void;
  href?: string;
  children?: ReactNode;
  accent?: boolean;
};

export function StatCard({
  title,
  subtitle,
  actionLabel,
  onActionClick,
  href,
  children,
  accent,
}: StatCardProps) {
  return (
    <Card tone={accent ? "accent" : "neutral"} className="space-y-3">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm font-semibold text-emerald-300">{subtitle}</p>
          <h3 className={cn("text-xl font-semibold", !subtitle && "mt-1")}>{title}</h3>
        </div>
        {actionLabel ? (
          <Button
            href={href}
            onClick={onActionClick}
            variant={accent ? "primary" : "secondary"}
            size="md"
          >
            {actionLabel}
          </Button>
        ) : null}
      </div>
      {children}
    </Card>
  );
}
