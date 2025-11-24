export type AuthPayload = {
  email: string;
  password: string;
  name?: string;
};

export type AuthResponse =
  | { ok: true; userId: string }
  | { ok: false; error: string };

// Placeholder auth calls; replace with Firebase/Backend wiring.
export async function login(payload: AuthPayload): Promise<AuthResponse> {
  await delay();
  if (!payload.email || !payload.password) {
    return { ok: false, error: "Missing credentials" };
  }
  return { ok: true, userId: "mock-user-id" };
}

export async function signup(payload: AuthPayload): Promise<AuthResponse> {
  await delay();
  if (!payload.email || !payload.password) {
    return { ok: false, error: "Missing credentials" };
  }
  return { ok: true, userId: "mock-user-id" };
}

function delay(ms = 500) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
