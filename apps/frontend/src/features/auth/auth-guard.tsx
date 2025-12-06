"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAppDispatch, useAppSelector } from "@/store/hooks";
import { me } from "@/features/auth/store/thunks";
import VerificationBanner from "@/features/auth/components/verification-banner";

type AuthGuardProps = {
  children: React.ReactNode;
};

const AuthGuard = ({ children }: AuthGuardProps) => {
  const dispatch = useAppDispatch();
  const router = useRouter();
  const { status } = useAppSelector((state) => state.auth);

  useEffect(() => {
    dispatch(me()).unwrap().catch(() => {
      router.replace("/login");
    });
  }, [dispatch, router]);

  if (status === "loading" || status === "idle") {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-sm text-muted-foreground">Checking session...</p>
      </div>
    );
  }

  if (status === "unauthenticated") {
    return null;
  }

  return (
    <>
      <VerificationBanner />
      {children}
    </>
  );
};

export default AuthGuard;
