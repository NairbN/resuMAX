import { useState } from "react";
import { optimizeResume, uploadResume } from "@/lib/api";
import {
  optimizeResumeMock,
  uploadResumeMock,
} from "@/lib/api-mock";

type UploadResult = {
  resumeId: string;
  originalUrl?: string;
  optimizedUrl?: string;
};

export function useUploadResume(userId?: string) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<UploadResult | null>(null);
  const useMock = process.env.NEXT_PUBLIC_USE_MOCK_API === "true";

  async function handleUpload(file: File, jobDescription?: string, jobTitle?: string, company?: string) {
    if (!userId) {
      setError("User not available");
      return;
    }
    setError(null);
    setLoading(true);
    setResult(null);

    try {
      const uploadRes = useMock
        ? await uploadResumeMock({ userId, file })
        : await uploadResume({ userId, file });

      const resumeId = uploadRes.resume_id || uploadRes.resumeId || "unknown";
      let optimizedUrl: string | undefined;

      if (jobDescription) {
        const optimizeRes = useMock
          ? await optimizeResumeMock({
              userId,
              resumeId,
              jobDescription,
              jobTitle,
              company,
            })
          : await optimizeResume({
              userId,
              resumeId,
              jobDescription,
              jobTitle,
              company,
            });
        optimizedUrl = optimizeRes.optimized_file_url || optimizeRes.optimizedUrl;
      }

      setResult({
        resumeId,
        originalUrl: uploadRes.original_file_url,
        optimizedUrl,
      });
    } catch (err: any) {
      setError(err?.message || "Failed to upload resume");
    } finally {
      setLoading(false);
    }
  }

  return { loading, error, result, handleUpload };
}
