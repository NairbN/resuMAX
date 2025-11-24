import { useState, useTransition } from "react";
import { useRouter } from "next/navigation";
import { login, signup } from "@/app/(auth)/lib/auth-client";
import { routes } from "@/lib/routes";

type Mode = "login" | "signup";

type UseAuthFormArgs = {
  mode: Mode;
  onSuccess?: () => void;
};

export function useAuthForm({ mode, onSuccess }: UseAuthFormArgs) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [, startTransition] = useTransition();
  const router = useRouter();

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setLoading(true);

    const formData = new FormData(event.currentTarget);
    const email = String(formData.get("email") || "").trim();
    const password = String(formData.get("password") || "");
    const name = String(formData.get("name") || "").trim();

    const result =
      mode === "login"
        ? await login({ email, password })
        : await signup({ name, email, password });

    if (!result.ok) {
      setError(result.error);
      setLoading(false);
      return;
    }

    console.log(`[auth] ${mode} success (client)`, { userId: result.userId });

    startTransition(() => {
      // Temporary session indicator for middleware; replace with real session cookie once backend sets it.
      document.cookie = "auth-token=client-session; path=/;";
      setLoading(false);
      if (onSuccess) {
        onSuccess();
      } else {
        router.push(routes.dashboard);
      }
    });
  }

  return { loading, error, handleSubmit };
}
