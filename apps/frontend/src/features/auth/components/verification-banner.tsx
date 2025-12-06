"use client";

import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { useAppDispatch, useAppSelector } from "@/store/hooks";
import { resendVerification } from "@/features/auth/store/thunks";

const VerificationBanner = () => {
  const dispatch = useAppDispatch();
  const { needsVerification, status, error } = useAppSelector(
    (state) => state.auth
  );

  if (!needsVerification) return null;

  const isPending = status === "loading";

  const handleResend = () => {
    dispatch(resendVerification());
  };

  return (
    <Alert variant="destructive" className="shadow-lg">
      <AlertTitle>Email not verified</AlertTitle>
      <AlertDescription className="flex items-center justify-between gap-3">
        <span>Check your inbox or resend the verification email.</span>
        <Button size="sm" onClick={handleResend} disabled={isPending}>
          {isPending ? "Sending..." : "Resend"}
        </Button>
      </AlertDescription>
      {error && (
        <p className="text-sm text-destructive mt-2 text-left">{error}</p>
      )}
    </Alert>
  );
};

export default VerificationBanner;
