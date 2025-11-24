"use client";
import Link from "next/link";
import { useState } from "react";
import { Button } from "@/components/Button";
import { FormField } from "@/app/(auth)/components/FormField";
import { AuthCard } from "@/app/(auth)/components/AuthCard";
import { AuthShell } from "@/app/(auth)/components/AuthShell";
import { useAuthForm } from "@/app/(auth)/hooks/useAuthForm";
import { routes } from "@/lib/routes";

export default function SignupPage() {
  const { loading, error, handleSubmit } = useAuthForm({ mode: "signup" });

  return (
    <AuthShell
      title="Start optimizing your resume with AI"
      description="Set up your workspace so we can tailor scoring, rewrites, and keyword matching to the roles you care about."
      pillText="Create your account"
    >
      <AuthCard accent>
        <form className="space-y-4" onSubmit={handleSubmit}>
          <FormField
            label="Full name"
            id="name"
            name="name"
            type="text"
            autoComplete="name"
            required
            placeholder="Alex Johnson"
            disabled={loading}
          />

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
            autoComplete="new-password"
            required
            placeholder="Create a strong password"
            disabled={loading}
          />

          {error ? <p className="text-sm text-rose-300">{error}</p> : null}

          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? "Creating account..." : "Create account"}
          </Button>
        </form>

        <p className="mt-6 text-sm text-white/70">
          Already have an account?{" "}
          <Link href={routes.login} className="font-semibold text-emerald-200 hover:text-emerald-100">
            Log in
          </Link>
        </p>
      </AuthCard>
    </AuthShell>
  );
}
