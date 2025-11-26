"use client";

import { WorkspaceShell } from "@/app/workspace/components/WorkspaceShell";
import { Navbar } from "@/app/workspace/components/Navbar";
import { Card } from "@/components/Card";
import { Button } from "@/components/Button";
import { listResumes, optimizeResume, deleteResume } from "@/lib/api";
import { useEffect, useState } from "react";

export default function OptimizePage() {
  const [resumes, setResumes] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedResumeId, setSelectedResumeId] = useState<string | null>(null);
  const [jobDescription, setJobDescription] = useState("");
  const [jobTitle, setJobTitle] = useState("");
  const [optimizing, setOptimizing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<any | null>(null);

  useEffect(() => {
    loadResumes();
  }, []);

  const loadResumes = async () => {
    try {
      setLoading(true);
      const data = await listResumes();
      setResumes(data);
    } catch (err: any) {
      setError(err.message || "Failed to load resumes");
    } finally {
      setLoading(false);
    }
  };

  const handleOptimize = async () => {
    if (!selectedResumeId || !jobDescription.trim()) return;

    setOptimizing(true);
    setError(null);
    setResult(null);

    try {
      const optimizeRes = await optimizeResume({
        resumeId: selectedResumeId,
        jobDescription: jobDescription.trim(),
        jobTitle: jobTitle.trim() || undefined,
      });
      setResult(optimizeRes);
    } catch (err: any) {
      setError(err.message || "Failed to optimize resume");
    } finally {
      setOptimizing(false);
    }
  };

  const handleDelete = async (resumeId: string) => {
    if (!confirm("Are you sure you want to delete this resume? This action cannot be undone.")) {
      return;
    }

    try {
      await deleteResume(resumeId);

      // If the deleted resume was selected, clear selection
      if (selectedResumeId === resumeId) {
        setSelectedResumeId(null);
        setJobDescription("");
        setJobTitle("");
        setResult(null);
      }

      // Reload resumes list
      await loadResumes();
    } catch (err: any) {
      setError(err.message || "Failed to delete resume");
    }
  };

  return (
    <WorkspaceShell>
      <Navbar />

      <div className="max-w-3xl space-y-6">
        <div>
          <h1 className="text-2xl font-semibold text-white">Optimize Resume</h1>
          <p className="mt-2 text-sm text-white/70">
            Select a resume and paste a job description to optimize it with semantic matching.
          </p>
        </div>

        {/* Step 1: Select Resume */}
        <Card tone="neutral" className="space-y-4">
          <h2 className="text-lg font-semibold text-white">1. Select Resume</h2>

          {loading ? (
            <p className="text-sm text-white/70">Loading your resumes...</p>
          ) : resumes.length === 0 ? (
            <div className="space-y-3">
              <p className="text-sm text-white/70">You haven't uploaded any resumes yet.</p>
              <Button variant="primary" href="/upload?returnTo=/optimize">
                Upload Your First Resume
              </Button>
            </div>
          ) : (
            <div className="space-y-2">
              {resumes.map((resume) => (
                <div
                  key={resume.resumeId}
                  className={`
                    p-4 rounded-xl border transition-all
                    ${selectedResumeId === resume.resumeId
                      ? 'border-emerald-300 bg-emerald-900/20'
                      : 'border-white/12 bg-white/5'
                    }
                  `}
                >
                  <div className="flex justify-between items-start gap-4">
                    <div
                      onClick={() => setSelectedResumeId(resume.resumeId)}
                      className="flex-1 cursor-pointer"
                    >
                      <p className="font-medium text-white">
                        {resume.originalFileName || 'Untitled Resume'}
                      </p>
                      <p className="text-xs text-white/60 mt-1">
                        Uploaded {new Date(resume.uploadedAt).toLocaleDateString()}
                      </p>
                      {resume.bulletCount && (
                        <p className="text-xs text-white/50 mt-1">
                          {resume.bulletCount} bullet points
                        </p>
                      )}
                    </div>
                    <div className="flex items-center gap-2">
                      {selectedResumeId === resume.resumeId && (
                        <span className="text-emerald-300 text-sm font-semibold">✓ Selected</span>
                      )}
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          handleDelete(resume.resumeId);
                        }}
                        className="text-rose-400 hover:text-rose-300 text-sm px-2 py-1 rounded hover:bg-rose-400/10 transition-colors"
                        title="Delete resume"
                      >
                        🗑️ Delete
                      </button>
                    </div>
                  </div>
                </div>
              ))}

              <p className="text-xs text-white/50 mt-2">
                You can have up to 5 resumes at a time
              </p>
            </div>
          )}
        </Card>

        {/* Step 2: Job Description (only show if resume selected) */}
        {selectedResumeId && (
          <Card tone="neutral" className="space-y-4">
            <h2 className="text-lg font-semibold text-white">2. Add Job Description</h2>

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
                rows={12}
                placeholder="Paste the complete job description here..."
                className="w-full rounded-xl border border-white/12 bg-white/5 px-4 py-3 text-white placeholder:text-white/50 focus:border-emerald-300 focus:outline-none focus:ring-2 focus:ring-emerald-300/30 resize-y font-mono text-sm"
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                disabled={optimizing}
              />
              <p className="text-xs text-white/50">
                Include the full job posting for best semantic matching results
              </p>
            </div>

            {error && (
              <p className="text-sm text-rose-300">{error}</p>
            )}

            <Button
              type="button"
              className="w-full"
              disabled={!jobDescription.trim() || optimizing}
              onClick={handleOptimize}
            >
              {optimizing ? "Optimizing..." : "🚀 Optimize Resume"}
            </Button>
          </Card>
        )}

        {/* Results */}
        {result && (
          <Card tone="accent" className="space-y-4">
            <h2 className="text-lg font-semibold text-emerald-300">✅ Optimization Complete!</h2>

            {result.relevance_scores?.comparison && (
              <div className="space-y-3 p-4 rounded-xl bg-white/5">
                <div className="flex justify-between text-sm">
                  <span className="text-white/80">Before Score:</span>
                  <span className="font-semibold text-white">
                    {result.relevance_scores.comparison.original_score?.toFixed(1)}%
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-white/80">After Score:</span>
                  <span className="font-semibold text-emerald-300">
                    {result.relevance_scores.comparison.optimized_score?.toFixed(1)}%
                  </span>
                </div>
                <div className="flex justify-between text-sm border-t border-white/10 pt-2">
                  <span className="text-white/80">Improvement:</span>
                  <span className="font-semibold text-emerald-300 text-lg">
                    +{result.relevance_scores.comparison.improvement?.toFixed(1)}%
                  </span>
                </div>
              </div>
            )}

            {result.relevance_scores?.comparison?.message && (
              <p className="text-sm text-white/90 italic">
                {result.relevance_scores.comparison.message}
              </p>
            )}

            <Button
              variant="secondary"
              className="w-full"
              onClick={async () => {
                if (!selectedResumeId) return;

                try {
                  // Use fetch with proper Authorization header
                  const USE_MOCK = process.env.NEXT_PUBLIC_USE_MOCK_AUTH === "true";
                  const headers: HeadersInit = {};

                  if (USE_MOCK) {
                    headers.Authorization = "Bearer mock-token-for-testing";
                  } else {
                    const { auth } = await import("@/lib/firebase");
                    const user = auth.currentUser;
                    if (user) {
                      const token = await user.getIdToken();
                      headers.Authorization = `Bearer ${token}`;
                    }
                  }

                  const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8080';
                  const downloadUrl = `${API_BASE}/download-resume/${selectedResumeId}?version=optimized`;
                  const response = await fetch(downloadUrl, { headers });

                  if (!response.ok) {
                    throw new Error(`Download failed: ${response.statusText}`);
                  }

                  // Get the blob and create download link
                  const blob = await response.blob();
                  const url = window.URL.createObjectURL(blob);
                  const link = document.createElement('a');
                  link.href = url;
                  link.download = 'optimized-resume.pdf';
                  document.body.appendChild(link);
                  link.click();
                  document.body.removeChild(link);
                  window.URL.revokeObjectURL(url);
                } catch (err) {
                  console.error('Download failed:', err);
                  alert('Failed to download resume');
                }
              }}
            >
              📥 Download Optimized Resume
            </Button>

            <Button
              variant="secondary"
              className="w-full"
              onClick={() => {
                setResult(null);
                setJobDescription("");
                setJobTitle("");
              }}
            >
              Optimize Another Resume
            </Button>
          </Card>
        )}
      </div>
    </WorkspaceShell>
  );
}
