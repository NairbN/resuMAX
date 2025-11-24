import type { AuthPayload, AuthResponse } from "./client";

type StoredUser = {
  email: string;
  password: string;
  name?: string;
};

const users = new Map<string, StoredUser>();
users.set("demo@resumax.ai", {
  email: "demo@resumax.ai",
  password: "password123",
  name: "Demo User",
});

export async function login(payload: AuthPayload): Promise<AuthResponse> {
  await delay();
  const email = (payload.email || "").toLowerCase();
  const user = users.get(email);

  if (!user || user.password !== payload.password) {
    return { ok: false, error: "Invalid email or password" };
  }

  return { ok: true, userId: email };
}

export async function signup(payload: AuthPayload): Promise<AuthResponse> {
  await delay();
  const email = (payload.email || "").toLowerCase();

  if (!email || !payload.password) {
    return { ok: false, error: "Missing credentials" };
  }

  if (users.has(email)) {
    return { ok: false, error: "Account already exists" };
  }

  users.set(email, {
    email,
    password: payload.password,
    name: payload.name,
  });

  return { ok: true, userId: email };
}

export async function logout(): Promise<void> {
  await delay();
  return;
}

function delay(ms = 500) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
