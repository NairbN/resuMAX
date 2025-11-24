"use client";
import Link from "next/link";
import { useState } from "react";
import { Button } from "@/components/Button";
import { FormField } from "@/app/(auth)/components/FormField";
import { AuthCard } from "@/app/(auth)/components/AuthCard";
import { AuthShell } from "@/app/(auth)/components/AuthShell";
import { useAuthForm } from "@/app/(auth)/hooks/useAuthForm";
import { routes } from "@/lib/routes";

export default function LoginPage() {
  const { loading, error, handleSubmit } = useAuthForm({ mode: "login" });

  return (
    <AuthShell
      title="Log in to your workspace"
      description="Pick up where you left off with saved drafts, role-specific scoring, and recruiter-ready exports."
      pillText="Welcome back"
    >
      <AuthCard>
        <form className="space-y-4" onSubmit={handleSubmit}>
          <FormField
            label="Email"
            id="email"
            name="email"
            type="email"
            autoComplete="email"
            required
            placeholder="you@example.com"
            disabled={loading}
          />

          <FormField
            label="Password"
            id="password"
            name="password"
            type="password"
            autoComplete="current-password"
            required
            placeholder="••••••••"
            disabled={loading}
          />

          <div className="flex items-center justify-between text-sm text-white/70">
            <label className="inline-flex items-center gap-2">
              <input
                type="checkbox"
                name="remember"
                className="h-4 w-4 rounded border-white/20 bg-white/5 text-emerald-400 focus:ring-2 focus:ring-emerald-300/60"
                disabled={loading}
              />
              <span>Remember me</span>
            </label>
            <Link href="#" className="text-emerald-200 hover:text-emerald-100">
              Forgot password?
            </Link>
          </div>

          {error ? <p className="text-sm text-rose-300">{error}</p> : null}

          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? "Logging in..." : "Log in"}
          </Button>
        </form>

        <p className="mt-6 text-sm text-white/70">
          New to resuMAX?{" "}
          <Link href={routes.signup} className="font-semibold text-emerald-200 hover:text-emerald-100">
            Create an account
          </Link>
        </p>
      </AuthCard>
    </AuthShell>
  );
}
