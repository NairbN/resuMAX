"use client";
import { Button } from "@/components/Button";
import { Card } from "@/components/Card";
import { Callout } from "@/components/Callout";
import { ListItem } from "@/components/ListItem";
import { Pill } from "@/components/Pill";
import { SectionHeader } from "@/components/SectionHeader";
import { DashboardShell } from "@/app/(dashboard)/components/DashboardShell";
import { Navbar } from "@/app/(dashboard)/components/Navbar";
import { StatCard } from "@/app/(dashboard)/components/StatCard";
import { useDashboardData } from "@/app/(dashboard)/hooks/useDashboardData";
import { routes } from "@/lib/routes";

export default function DashboardPage() {
  const userId = process.env.NEXT_PUBLIC_DEMO_USER_ID || "demo-user";
  const data = useDashboardData(userId);

  return (
    <DashboardShell>
      <Navbar />

      <div className="flex flex-col gap-4">
        <Pill>
          <span className="font-medium text-emerald-300">resuMAX</span>
          <span className="text-white/80">Your AI resume hub</span>
        </Pill>
        <SectionHeader
          title="Welcome back. Let's keep your resume moving."
          description="Upload a new resume, add job descriptions, and review your latest optimizations. All your steps stay in sync."
        />
      </div>

      {!data ? (
        <Callout title="Loading dashboard...">Fetching your data.</Callout>
      ) : (
        <>
          <div className="grid gap-6 lg:grid-cols-2">
            <StatCard
              title="Upload Resume"
              subtitle="Resume status"
              actionLabel="Upload your resume"
              href={routes.upload}
            >
              <p className="text-sm text-white/80">Last uploaded: {data.lastUpload.date}</p>
              <p className="text-sm text-emerald-300">
                Status: {data.lastUpload.status === "parsed" ? "Parsed" : "Not parsed"}
              </p>
            </StatCard>

            <StatCard
              title="Your Profile Summary"
              subtitle="Snapshot"
              actionLabel="View Profile"
              href={routes.dashboard}
            >
              <div className="flex items-center gap-6 text-sm text-white/80">
                <span>Experiences: {data.profileSnapshot.experiences}</span>
                <span>Skills: {data.profileSnapshot.skills}</span>
                <span>Projects: {data.profileSnapshot.projects}</span>
              </div>
            </StatCard>

            <StatCard
              title="Add Job Description"
              subtitle="Targets"
              actionLabel="Add Job Description"
              href="#"
              accent
            >
              <p className="text-sm text-white/80">Recent jobs:</p>
              <ul className="mt-2 space-y-1 text-sm text-white/80">
                {data.recentJobs.map((job) => (
                  <li key={job.id} className="flex items-center gap-2">
                    <span className="h-2 w-2 rounded-full bg-emerald-300" aria-hidden />
                    <span>{job.title}</span>
                  </li>
                ))}
              </ul>
            </StatCard>

            <Card tone="muted" className="space-y-3">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <p className="text-sm font-semibold text-emerald-300">Recent Optimizations</p>
                  <h3 className="text-xl font-semibold">Your last 3 optimized resumes</h3>
                </div>
                <Button variant="secondary" href="#">
                  View All
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
    </DashboardShell>
  );
}
