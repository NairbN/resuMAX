import { useRouter, useSearchParams } from "next/navigation";
import { useState } from "react";
import { Button } from "@/components/Button";
import { Card } from "@/components/Card";
import { useUploadResume } from "../hooks/useUploadResume";
import { optimizeResume } from "@/lib/api";

type UploadFormProps = {
  userId: string;
};

export function UploadForm({ userId }: UploadFormProps) {
  const { loading, error, result, handleUpload } = useUploadResume(userId);
  const router = useRouter();
  const searchParams = useSearchParams();
  const returnTo = searchParams.get('returnTo') || '/workspace';
  const [file, setFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState<string>("");
  const [jobTitle, setJobTitle] = useState<string>("");
  const [optimizing, setOptimizing] = useState(false);
  const [optimizeError, setOptimizeError] = useState<string | null>(null);
  const [optimizeResult, setOptimizeResult] = useState<any | null>(null);

  return (
    <Card tone="neutral" className="space-y-4">
      <form
        className="space-y-4"
        onSubmit={(e) => {
          e.preventDefault();
          if (!file) return;
          handleUpload(file).then((res) => {
            if (res?.resumeId) {
              // Redirect back to where they came from (optimize or workspace)
              router.push(returnTo);
            }
          });
        }}
      >
        <div className="space-y-2">
          <label className="text-sm font-medium text-white/90" htmlFor="resume">
            Resume file (PDF)
          </label>
          <input
            id="resume"
            name="resume"
            type="file"
            accept=".pdf,application/pdf"
            className="w-full rounded-xl border border-white/12 bg-white/5 px-4 py-3 text-white placeholder:text-white/50 focus:border-emerald-300 focus:outline-none focus:ring-2 focus:ring-emerald-300/30"
            disabled={loading}
            onChange={(e) => {
              const picked = e.target.files?.[0] || null;
              setFile(picked);
            }}
          />
          {file ? (
            <p className="text-sm text-white/70">Selected: {file.name}</p>
          ) : (
            <p className="text-sm text-white/50">Max 10MB. Accepted: PDF only.</p>
          )}
        </div>

        {error ? <p className="text-sm text-rose-300">{error}</p> : null}

        <Button type="submit" className="w-full" disabled={!file || loading}>
          {loading ? "Uploading..." : "Upload"}
        </Button>
      </form>

      {result ? (
        <div className="rounded-xl border border-white/10 bg-white/5 p-4 text-sm text-white/80">
          <p className="font-semibold text-white">Upload complete</p>
          <p className="mt-1">Resume ID: {result.resumeId}</p>
          {result.originalUrl ? (
            <p className="mt-1">
              Original: <span className="text-emerald-200">{result.originalUrl}</span>
            </p>
          ) : null}
        </div>
      ) : null}

      {/* Job Description Section - Only show after resume is uploaded */}
      {result?.resumeId && (
        <>
          <div className="border-t border-white/10 my-6"></div>

          <div className="space-y-4">
            <h2 className="text-lg font-semibold text-white">Optimize for a Job</h2>
            <p className="text-sm text-white/70">
              Paste the job description below to optimize your resume with semantic matching.
            </p>

            <div className="space-y-2">
              <label className="text-sm font-medium text-white/90" htmlFor="jobTitle">
                Job Title (optional)
              </label>
              <input
                id="jobTitle"
                type="text"
                placeholder="e.g., Senior Software Engineer"
                className="w-full rounded-xl border border-white/12 bg-white/5 px-4 py-3 text-white placeholder:text-white/50 focus:border-emerald-300 focus:outline-none focus:ring-2 focus:ring-emerald-300/30"
                value={jobTitle}
                onChange={(e) => setJobTitle(e.target.value)}
                disabled={optimizing}
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-white/90" htmlFor="jobDescription">
                Job Description *
              </label>
              <textarea
                id="jobDescription"
                rows={10}
                placeholder="Paste the full job description here..."
                className="w-full rounded-xl border border-white/12 bg-white/5 px-4 py-3 text-white placeholder:text-white/50 focus:border-emerald-300 focus:outline-none focus:ring-2 focus:ring-emerald-300/30 resize-y"
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                disabled={optimizing}
              />
              <p className="text-xs text-white/50">
                Paste the complete job posting for best results
              </p>
            </div>

            {optimizeError && (
              <p className="text-sm text-rose-300">{optimizeError}</p>
            )}

            <Button
              type="button"
              className="w-full"
              disabled={!jobDescription.trim() || optimizing}
              onClick={async () => {
                if (!jobDescription.trim() || !result?.resumeId) return;

                setOptimizing(true);
                setOptimizeError(null);
                setOptimizeResult(null);

                try {
                  const optimizeRes = await optimizeResume({
                    resumeId: result.resumeId,
                    jobDescription: jobDescription.trim(),
                    jobTitle: jobTitle.trim() || undefined,
                  });
                  setOptimizeResult(optimizeRes);
                } catch (err: any) {
                  setOptimizeError(err.message || "Failed to optimize resume");
                } finally {
                  setOptimizing(false);
                }
              }}
            >
              {optimizing ? "Optimizing..." : "🚀 Optimize Resume"}
            </Button>

            {optimizeResult && (
              <div className="rounded-xl border border-emerald-300/30 bg-emerald-900/20 p-4 space-y-3">
                <p className="font-semibold text-emerald-300">✅ Optimization Complete!</p>

                {optimizeResult.relevance_scores && (
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="text-white/80">Before Score:</span>
                      <span className="font-semibold text-white">
                        {optimizeResult.relevance_scores.original_score?.toFixed(1)}%
                      </span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-white/80">After Score:</span>
                      <span className="font-semibold text-emerald-300">
                        {optimizeResult.relevance_scores.optimized_score?.toFixed(1)}%
                      </span>
                    </div>
                    <div className="flex justify-between text-sm border-t border-white/10 pt-2">
                      <span className="text-white/80">Improvement:</span>
                      <span className="font-semibold text-emerald-300">
                        +{optimizeResult.relevance_scores.improvement?.toFixed(1)}%
                      </span>
                    </div>
                  </div>
                )}

                {optimizeResult.relevance_scores?.message && (
                  <p className="text-sm text-white/80 italic">
                    {optimizeResult.relevance_scores.message}
                  </p>
                )}

                {optimizeResult.optimized_file_url && (
                  <Button
                    variant="secondary"
                    className="w-full mt-4"
                    onClick={() => {
                      window.open(optimizeResult.optimized_file_url, '_blank');
                    }}
                  >
                    📥 Download Optimized Resume
                  </Button>
                )}
              </div>
            )}
          </div>
        </>
      )}
    </Card>
  );
}
