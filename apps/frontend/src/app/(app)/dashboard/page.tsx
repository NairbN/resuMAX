"use client";

import LogoutButton from "@/features/auth/components/logout-button";
import { useAppSelector } from "@/store/hooks";
import { Button } from "@/components/ui/button";

const DashboardPage = () => {
  return (
    <main className="p-8 space-y-4">
      <div className="flex items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold">Dashboard</h1>
          <p className="text-sm text-gray-600">
            Status cards and recent activity will go here.
          </p>
        </div>
        <LogoutButton />
      </div>
      <DashboardActions />
    </main>
  );
};

const DashboardActions = () => {
  const { needsVerification } = useAppSelector((state) => state.auth);

  return (
    <div className="rounded-lg border p-4 space-y-3">
      <div className="flex items-center justify-between">
        <div>
          <p className="font-medium">Resume upload</p>
          <p className="text-sm text-muted-foreground">
            Upload your resume to start optimizing.
          </p>
        </div>
        <Button disabled={needsVerification}>Go to upload</Button>
      </div>
      {needsVerification && (
        <p className="text-sm text-destructive">
          Verify your email to enable uploads.
        </p>
      )}
    </div>
  );
};

export default DashboardPage;
