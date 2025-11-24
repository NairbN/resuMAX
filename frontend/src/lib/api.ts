const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL;

export type ResumeMetadata = {
  userId: string;
  resumeId: string;
  originalFileName?: string;
  originalFile?: string;
  uploadedAt?: string;
  optimizedAt?: string;
  status?: string;
  relevanceScore?: number;
  jobTitle?: string;
  company?: string;
};

export async function listResumes(userId: string): Promise<ResumeMetadata[]> {
  if (!API_BASE) throw new Error("API base URL is not configured");

  const res = await fetch(`${API_BASE}/resumes/${encodeURIComponent(userId)}`, {
    method: "GET",
  });
  if (!res.ok) {
    throw new Error(`Failed to list resumes: ${res.status}`);
  }
  const data = (await res.json()) as { resumes?: ResumeMetadata[] };
  return data.resumes || [];
}

export async function uploadResume(params: {
  userId: string;
  file: File;
}): Promise<any> {
  if (!API_BASE) throw new Error("API base URL is not configured");

  const formData = new FormData();
  formData.append("user_id", params.userId);
  formData.append("file", params.file);

  const res = await fetch(`${API_BASE}/upload-resume`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Failed to upload resume: ${res.status} ${text}`);
  }

  return res.json();
}

export async function optimizeResume(params: {
  userId: string;
  resumeId: string;
  jobDescription: string;
  jobTitle?: string;
  company?: string;
}): Promise<any> {
  if (!API_BASE) throw new Error("API base URL is not configured");

  const res = await fetch(`${API_BASE}/job-description`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_id: params.userId,
      resume_id: params.resumeId,
      job_description: params.jobDescription,
      job_title: params.jobTitle,
      company: params.company,
    }),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Failed to optimize resume: ${res.status} ${text}`);
  }

  return res.json();
}

export function getDownloadResumeUrl(params: {
  userId: string;
  resumeId: string;
  version?: "original" | "optimized";
}): string {
  const version = params.version || "optimized";
  if (!API_BASE) throw new Error("API base URL is not configured");
  return `${API_BASE}/download-resume/${encodeURIComponent(params.resumeId)}?user_id=${encodeURIComponent(params.userId)}&version=${encodeURIComponent(version)}`;
}
