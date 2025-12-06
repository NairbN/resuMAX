"use client";

import { useEffect, useMemo, useState } from "react";
import { Button } from "@/components/ui/button";
import AuthModal from "@/features/auth/components/auth-modal";
import AuthCtaButtons from "@/features/auth/components/auth-cta-buttons";
import { Logo } from "@/components/logo";
import MockControls from "@/features/auth/components/mock-controls";

type ModalMode = "login" | "signup" | null;

export default function Home() {
  const [mode, setMode] = useState<ModalMode>(null);
  const [scrollY, setScrollY] = useState(0);
  const isMock = process.env.NEXT_PUBLIC_USE_AUTH_MOCK === "true";
  const [mockOpen, setMockOpen] = useState(false);

  const closeModal = () => setMode(null);

  useEffect(() => {
    const onScroll = () => setScrollY(window.scrollY || 0);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  const { mainOpacity, cornerOpacity } = useMemo(() => {
    const main = Math.max(0, Math.min(1, 1 - scrollY / 200));
    const corner = Math.max(0, Math.min(1, (scrollY - 80) / 200));
    return { mainOpacity: main, cornerOpacity: corner };
  }, [scrollY]);

  return (
    <div className="relative min-h-[200vh] bg-gradient-to-br from-slate-50 via-white to-slate-100 text-slate-900 dark:from-slate-800 dark:via-slate-900 dark:to-slate-950 dark:text-white">
      <div className="fixed right-4 top-4 flex items-center gap-3 z-20">
        <div
          className="flex gap-2 transition-opacity duration-200"
          style={{
            opacity: cornerOpacity,
            pointerEvents: cornerOpacity > 0.05 ? "auto" : "none",
          }}
        >
          <Button
            size="sm"
            variant="outline"
            onClick={() => setMode("login")}
            className="bg-transparent border border-slate-300 text-slate-900 hover:bg-slate-100 hover:text-slate-900 dark:border-white/60 dark:text-white dark:hover:bg-white/10 dark:hover:text-white"
          >
            Log in
          </Button>
          <Button
            size="sm"
            variant="default"
            className="bg-primary text-primary-foreground hover:bg-primary/90"
            onClick={() => setMode("signup")}
          >
            Sign Up
          </Button>
        </div>
      </div>
      <div className="absolute inset-0 pointer-events-none" />
      <header className="mx-auto max-w-5xl px-6 py-16 text-center">
        <div className="mx-auto max-w-lg rounded-2xl border border-white/10 bg-white/10 dark:border-white/15 dark:bg-white/5 p-10 shadow-2xl backdrop-blur-sm">
          <div className="flex items-center justify-center py-6">
            <Logo size={320} className="drop-shadow-lg w-full h-auto" />
          </div>
        </div>
        <AuthCtaButtons
          onLogin={() => setMode("login")}
          onSignup={() => setMode("signup")}
          style={{
            opacity: mainOpacity,
            pointerEvents: mainOpacity > 0.05 ? "auto" : "none",
            transition: "opacity 200ms ease-in-out",
          }}
        />
      </header>

      <AuthModal
        open={mode !== null}
        mode={mode ?? "login"}
        onClose={closeModal}
        onSwitchMode={(next) => setMode(next)}
      />
      {isMock && <MockControls open={mockOpen} onClose={() => setMockOpen(false)} />}
    </div>
  );
}
