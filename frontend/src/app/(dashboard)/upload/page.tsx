"use client";

import { DashboardShell } from "@/app/(dashboard)/components/DashboardShell";
import { Navbar } from "@/app/(dashboard)/components/Navbar";
import { UploadForm } from "@/app/(dashboard)/upload/components/UploadForm";
import { Pill } from "@/components/Pill";
import { SectionHeader } from "@/components/SectionHeader";
import { routes } from "@/lib/routes";

export default function UploadPage() {
  const userId = process.env.NEXT_PUBLIC_DEMO_USER_ID || "demo-user";

  return (
    <DashboardShell>
      <Navbar />

      <div className="flex flex-col gap-4">
        <Pill>
          <span className="font-medium text-emerald-300">resuMAX</span>
          <span className="text-white/80">Upload & optimize</span>
        </Pill>
        <SectionHeader
          title="Upload a resume and kick off optimization"
          description="Choose a PDF or DOCX. Optionally paste a job description to auto-optimize after upload."
        />
      </div>

      <UploadForm userId={userId} />
    </DashboardShell>
  );
}
