import { auth } from "./firebase/client";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL;
const USE_MOCK = process.env.NEXT_PUBLIC_USE_MOCK_AUTH === "true";

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

async function getAuthHeaders(): Promise<HeadersInit> {
  // Mock mode: use a fake token (backend has LOCAL_TESTING=true so it accepts anything)
  if (USE_MOCK) {
    return {
      Authorization: `Bearer mock-token-for-testing`,
    };
  }

  // Real Firebase mode
  const user = auth.currentUser;
  if (!user) {
    throw new Error("Not authenticated");
  }
  const token = await user.getIdToken();
  return {
    Authorization: `Bearer ${token}`,
  };
}

export async function listResumes(): Promise<ResumeMetadata[]> {
  if (!API_BASE) throw new Error("API base URL is not configured");

  const headers = await getAuthHeaders();
  const res = await fetch(`${API_BASE}/resumes`, {
    method: "GET",
    headers,
  });
  if (!res.ok) {
    throw new Error(`Failed to list resumes: ${res.status}`);
  }
  const data = (await res.json()) as { resumes?: ResumeMetadata[] };
  return data.resumes || [];
}

export async function uploadResume(params: {
  file: File;
}): Promise<any> {
  if (!API_BASE) throw new Error("API base URL is not configured");

  const headers = await getAuthHeaders();
  const formData = new FormData();
  formData.append("file", params.file);

  const res = await fetch(`${API_BASE}/upload-resume`, {
    method: "POST",
    headers,
    body: formData,
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Failed to upload resume: ${res.status} ${text}`);
  }

  return res.json();
}

export async function optimizeResume(params: {
  resumeId: string;
  jobDescription: string;
  jobTitle?: string;
  company?: string;
}): Promise<any> {
  if (!API_BASE) throw new Error("API base URL is not configured");

  const authHeaders = await getAuthHeaders();
  const res = await fetch(`${API_BASE}/job-description`, {
    method: "POST",
    headers: {
      ...authHeaders,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
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

export async function getDownloadResumeUrl(params: {
  resumeId: string;
  version?: "original" | "optimized";
}): Promise<string> {
  const version = params.version || "optimized";
  if (!API_BASE) throw new Error("API base URL is not configured");

  let token: string;
  if (USE_MOCK) {
    token = "mock-token-for-testing";
  } else {
    const user = auth.currentUser;
    if (!user) throw new Error("Not authenticated");
    token = await user.getIdToken();
  }

  // Note: For download endpoints, we can pass the token as a query param since it's a direct link
  return `${API_BASE}/download-resume/${encodeURIComponent(params.resumeId)}?version=${encodeURIComponent(version)}&token=${encodeURIComponent(token)}`;
}

export async function deleteResume(resumeId: string): Promise<void> {
  if (!API_BASE) throw new Error("API base URL is not configured");

  const headers = await getAuthHeaders();
  const res = await fetch(`${API_BASE}/resume/${encodeURIComponent(resumeId)}`, {
    method: "DELETE",
    headers,
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Failed to delete resume: ${res.status} ${text}`);
  }
}
