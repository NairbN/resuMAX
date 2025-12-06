"use client";

import { Button } from "@/components/ui/button";
import { useAppSelector } from "@/store/hooks";

const UploadPage = () => {
  const { needsVerification } = useAppSelector((state) => state.auth);

  return (
    <main className="p-8 space-y-4">
      <h1 className="text-2xl font-semibold">Upload Resume</h1>
      <p className="text-sm text-gray-600">Presigned upload flow goes here.</p>
      <div className="rounded-lg border p-4 space-y-3">
        <div className="flex items-center justify-between">
          <div>
            <p className="font-medium">Upload your resume</p>
            <p className="text-sm text-muted-foreground">
              Only available after verifying your email.
            </p>
          </div>
          <Button disabled={needsVerification}>Upload file</Button>
        </div>
        {needsVerification && (
          <p className="text-sm text-destructive">
            Verify your email to enable uploads.
          </p>
        )}
      </div>
    </main>
  );
};

export default UploadPage;
