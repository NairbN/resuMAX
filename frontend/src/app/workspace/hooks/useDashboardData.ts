import { useEffect, useState } from "react";
import { DashboardData } from "../lib/dashboard";
import { getMockDashboardData } from "@/mocks/dashboard";
import { listResumes, type ResumeMetadata } from "@/lib/api";
import { listResumesMock } from "@/mocks/api";

function mapFromResumes(resumes: ResumeMetadata[]): DashboardData {
  if (!resumes.length) {
    return getMockDashboardData();
  }

  const mostRecent = resumes[0];
  const optimized = resumes.filter((r) => r.status === "optimized" || r.optimizedAt);

  return {
    lastUpload: {
      date: (mostRecent.uploadedAt || "").slice(0, 10) || "N/A",
      status: mostRecent.status === "optimized" ? "parsed" : "not_parsed",
    },
    profileSnapshot: {
      experiences: 0,
      skills: 0,
      projects: 0,
    },
    recentJobs: getMockDashboardData().recentJobs,
    recentOptimizations: optimized.slice(0, 3).map((item) => ({
      id: item.resumeId,
      title: item.originalFileName || item.jobTitle || "Resume",
      updatedAt: (item.optimizedAt || item.uploadedAt || "").slice(0, 10) || "N/A",
      score: item.relevanceScore ? Math.round(item.relevanceScore) : 0,
    })),
  };
}

export function useDashboardData(userId?: string) {
  const [data, setData] = useState<DashboardData | null>(null);
  const useMock = process.env.NEXT_PUBLIC_USE_MOCK_API === "true";

  useEffect(() => {
    let cancelled = false;

    async function load() {
      if (!userId || useMock) {
        const mockResumes = await listResumesMock(userId || "mock-user");
        setData(mapFromResumes(mockResumes));
        return;
      }
      try {
        const resumes = await listResumes();
        if (!cancelled) {
          setData(mapFromResumes(resumes));
        }
      } catch (error) {
        console.error("[workspace] failed to load resumes, falling back to mock", error);
        if (!cancelled) {
          setData(getMockDashboardData());
        }
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, [userId, useMock]);

  return data;
}
