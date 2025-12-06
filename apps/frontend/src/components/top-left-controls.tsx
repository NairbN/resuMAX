"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Moon, Sun } from "lucide-react";
import MockControls from "@/features/auth/components/mock-controls";

const TopLeftControls = () => {
  const [theme, setTheme] = useState<"light" | "dark">("light");
  const [mockOpen, setMockOpen] = useState(false);
  const isDark = theme === "dark";
  const isMock = process.env.NEXT_PUBLIC_USE_AUTH_MOCK === "true";

  useEffect(() => {
    const stored = window.localStorage.getItem("theme");
    if (stored === "dark" || stored === "light") {
      setTheme(stored);
    } else if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
      setTheme("dark");
    }
  }, []);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", theme === "dark");
    window.localStorage.setItem("theme", theme);
  }, [theme]);

  return (
    <>
      <div className="fixed left-4 top-4 z-50 flex items-center gap-2">
        <Button
          size="sm"
          variant="ghost"
          className={`border ${
            isDark
              ? "border-white/20 text-white hover:bg-white/10"
              : "border-slate-300 text-slate-900 hover:bg-slate-100"
          }`}
          onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
        >
          {theme === "dark" ? (
            <>
              <Sun className="mr-2 h-4 w-4" />
              Light
            </>
          ) : (
            <>
              <Moon className="mr-2 h-4 w-4" />
              Dark
            </>
          )}
        </Button>
        {isMock && (
          <Button
            size="sm"
            variant="outline"
            onClick={() => setMockOpen(true)}
            className={
              isDark
                ? "border border-white/60 text-white hover:bg-white/10 hover:text-white"
                : "border border-slate-300 text-slate-900 hover:bg-slate-100 hover:text-slate-900"
            }
          >
            Mock controls
          </Button>
        )}
      </div>
      {isMock && (
        <MockControls open={mockOpen} onClose={() => setMockOpen(false)} />
      )}
    </>
  );
};

export default TopLeftControls;
