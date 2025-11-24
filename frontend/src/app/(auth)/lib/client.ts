import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
} from "firebase/auth";
import { auth } from "@/lib/firebase/client";

export type AuthPayload = {
  email: string;
  password: string;
  name?: string;
};

export type AuthResponse =
  | { ok: true; userId: string }
  | { ok: false; error: string };

export async function login(payload: AuthPayload): Promise<AuthResponse> {
  try {
    if (!payload.email || !payload.password) {
      return { ok: false, error: "Missing credentials" };
    }
    const cred = await signInWithEmailAndPassword(auth, payload.email, payload.password);
    return { ok: true, userId: cred.user.uid };
  } catch (error: any) {
    return { ok: false, error: error?.message || "Unable to log in" };
  }
}

export async function signup(payload: AuthPayload): Promise<AuthResponse> {
  try {
    if (!payload.email || !payload.password) {
      return { ok: false, error: "Missing credentials" };
    }
    const cred = await createUserWithEmailAndPassword(auth, payload.email, payload.password);
    return { ok: true, userId: cred.user.uid };
  } catch (error: any) {
    return { ok: false, error: error?.message || "Unable to sign up" };
  }
}

export async function logout(): Promise<void> {
  await signOut(auth);
}
