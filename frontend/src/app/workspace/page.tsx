"use client";
import { Button } from "@/components/Button";
import { Card } from "@/components/Card";
import { Callout } from "@/components/Callout";
import { ListItem } from "@/components/ListItem";
import { WorkspaceShell } from "@/app/workspace/components/WorkspaceShell";
import { Navbar } from "@/app/workspace/components/Navbar";
import { useDashboardData } from "@/app/workspace/hooks/useDashboardData";
import { routes } from "@/lib/routes";

export default function DashboardPage() {
  const userId = process.env.NEXT_PUBLIC_DEMO_USER_ID || "demo-user";
  const data = useDashboardData(userId);

  return (
    <WorkspaceShell>
      <Navbar />

      {!data ? (
        <Callout title="Loading workspace...">Fetching your data.</Callout>
      ) : (
        <>
          <div className="space-y-6">
            <Card tone="accent" className="space-y-3">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <p className="text-sm font-semibold text-emerald-300">Add Job Description</p>
                  <h3 className="text-xl font-semibold">Target your next role</h3>
                  <p className="text-sm text-white/80">
                    Paste a job description to kick off optimization against your latest resume.
                  </p>
                </div>
                <Button variant="primary" href={routes.optimize}>
                  Add Job Description
                </Button>
              </div>
            </Card>

            <Card tone="muted" className="space-y-3">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <p className="text-sm font-semibold text-emerald-300">Recent Optimizations</p>
                  <h3 className="text-xl font-semibold">Your last 3 optimized resumes</h3>
                </div>
                <Button variant="secondary" href={routes.profile}>
                  View Profile
                </Button>
              </div>
              <ul className="space-y-2">
                {data.recentOptimizations.map((item) => (
                  <ListItem key={item.id} className="items-center">
                    <div className="flex flex-col">
                      <span className="font-medium text-white">{item.title}</span>
                      <span className="text-xs text-white/60">Updated {item.updatedAt}</span>
                    </div>
                    <span className="ml-auto text-sm font-semibold text-emerald-300">
                      Score {item.score}
                    </span>
                  </ListItem>
                ))}
              </ul>
            </Card>
          </div>
        </>
      )}
    </WorkspaceShell>
  );
}
