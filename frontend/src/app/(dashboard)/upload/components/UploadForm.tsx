import { useState } from "react";
import { Button } from "@/components/Button";
import { Card } from "@/components/Card";
import { FormField } from "@/app/(auth)/components/FormField";
import { useUploadResume } from "../hooks/useUploadResume";

type UploadFormProps = {
  userId: string;
};

export function UploadForm({ userId }: UploadFormProps) {
  const { loading, error, result, handleUpload } = useUploadResume(userId);
  const [file, setFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState("");
  const [jobTitle, setJobTitle] = useState("");
  const [company, setCompany] = useState("");

  return (
    <Card tone="neutral" className="space-y-4">
      <form
        className="space-y-4"
        onSubmit={(e) => {
          e.preventDefault();
          if (!file) return;
          handleUpload(file, jobDescription, jobTitle, company);
        }}
      >
        <div className="space-y-2">
          <label className="text-sm font-medium text-white/90" htmlFor="resume">
            Resume file (PDF or DOCX)
          </label>
          <input
            id="resume"
            name="resume"
            type="file"
            accept=".pdf,.doc,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
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
            <p className="text-sm text-white/50">Max 10MB. Accepted: PDF, DOCX.</p>
          )}
        </div>

        <FormField
          label="Job title (optional)"
          id="jobTitle"
          name="jobTitle"
          value={jobTitle}
          onChange={(e) => setJobTitle(e.target.value)}
          placeholder="Senior Product Manager"
          disabled={loading}
        />

        <FormField
          label="Company (optional)"
          id="company"
          name="company"
          value={company}
          onChange={(e) => setCompany(e.target.value)}
          placeholder="Acme Inc."
          disabled={loading}
        />

        <div className="space-y-2">
          <label className="text-sm font-medium text-white/90" htmlFor="jobDescription">
            Job description (optional)
          </label>
          <textarea
            id="jobDescription"
            name="jobDescription"
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            disabled={loading}
            rows={6}
            className="w-full rounded-xl border border-white/12 bg-white/5 px-4 py-3 text-white placeholder:text-white/50 focus:border-emerald-300 focus:outline-none focus:ring-2 focus:ring-emerald-300/30"
            placeholder="Paste a job description to kick off optimization automatically."
          />
        </div>

        {error ? <p className="text-sm text-rose-300">{error}</p> : null}

        <Button type="submit" className="w-full" disabled={!file || loading}>
          {loading ? "Uploading..." : "Upload and (optionally) optimize"}
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
          {result.optimizedUrl ? (
            <p className="mt-1">
              Optimized: <span className="text-emerald-200">{result.optimizedUrl}</span>
            </p>
          ) : (
            <p className="mt-1 text-white/60">No optimization requested.</p>
          )}
        </div>
      ) : null}
    </Card>
  );
}
