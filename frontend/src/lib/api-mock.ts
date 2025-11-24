import { getMockDashboardData } from "@/app/(dashboard)/lib/dashboard-data";

const mockData = getMockDashboardData();

export async function listResumesMock(userId: string) {
  console.log("[api-mock] listResumes", { userId });
  // Adapt dashboard mock data into a resume-like shape
  return mockData.recentOptimizations.map((item, idx) => ({
    userId,
    resumeId: item.id || `mock-resume-${idx + 1}`,
    originalFileName: item.title,
    uploadedAt: item.updatedAt,
    optimizedAt: item.updatedAt,
    status: "optimized",
    relevanceScore: item.score,
  }));
}

export async function uploadResumeMock(params: { userId: string; file: File }) {
  console.log("[api-mock] uploadResume", { userId: params.userId, file: params.file.name });
  return {
    resume_id: "mock-resume-uploaded",
    original_file_url: "gs://mock/resume.pdf",
    parsed_data: { bullet_count: 10, sections: ["experience", "skills"] },
  };
}

export async function optimizeResumeMock(params: {
  userId: string;
  resumeId: string;
  jobDescription: string;
  jobTitle?: string;
  company?: string;
}) {
  console.log("[api-mock] optimizeResume", params);
  return {
    resume_id: params.resumeId,
    optimized_file_url: "gs://mock/optimized.pdf",
    relevance_scores: { overall_score: 90 },
  };
}

export function getDownloadResumeUrlMock(params: {
  userId: string;
  resumeId: string;
  version?: "original" | "optimized";
}) {
  console.log("[api-mock] downloadResumeUrl", params);
  return "#";
}
