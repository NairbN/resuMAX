"use client";

import { Button } from "@/components/ui/button";
import { logout, login, verifyEmail } from "@/features/auth/store/thunks";
import { useAppDispatch, useAppSelector } from "@/store/hooks";
import { X } from "lucide-react";
import { useRouter } from "next/navigation";
import { setMockVerification } from "@/features/auth/api/mock";

type MockControlsProps = {
  open: boolean;
  onClose: () => void;
};

const MOCK_EMAIL = "mockuser@example.com";
const MOCK_PASSWORD = "password123";

const MockControls = ({ open, onClose }: MockControlsProps) => {
  const dispatch = useAppDispatch();
  const { needsVerification, status, user } = useAppSelector(
    (state) => state.auth
  );
  const router = useRouter();

  if (!open) return null;

  const handleLogin = async () => {
    // ensure starts unverified
    setMockVerification(false);
    await dispatch(
      login({ email: MOCK_EMAIL, password: MOCK_PASSWORD })
    ).unwrap();
    router.push("/dashboard");
  };

  const handleVerify = async () => {
    await dispatch(verifyEmail("mock-token")).unwrap();
  };

  const handleLogout = async () => {
    await dispatch(logout()).unwrap();
    router.push("/");
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center backdrop-blur bg-white/60 dark:bg-white/20">
      <div
        className="absolute inset-0"
        aria-label="Close mock controls"
        onClick={onClose}
      />
      <div className="relative w-full max-w-md mx-4 rounded-2xl border border-border bg-card text-card-foreground p-6 shadow-2xl">
        <button
          onClick={onClose}
          className="absolute right-3 top-3 rounded-full bg-foreground/10 p-1.5 text-foreground hover:bg-foreground/20"
          aria-label="Close"
        >
          <X className="h-4 w-4" />
        </button>
        <div className="space-y-2 mb-4">
          <p className="text-sm uppercase tracking-[0.2em] text-muted-foreground">
            Mock controls
          </p>
          <p className="text-sm text-muted-foreground">
            Status: {status}
            {user?.email ? ` • ${user.email}` : ""}{" "}
            {needsVerification ? "• needs verification" : ""}
          </p>
        </div>
        <div className="grid gap-3">
          <Button onClick={handleLogin} className="w-full">
            Quick log in as {MOCK_EMAIL}
          </Button>
          <Button variant="outline" onClick={handleVerify} className="w-full">
            Mark account verified
          </Button>
          <Button variant="outline" onClick={handleLogout} className="w-full">
            Log out
          </Button>
        </div>
      </div>
    </div>
  );
};

export default MockControls;
