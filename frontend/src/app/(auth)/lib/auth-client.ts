import * as real from "./client";
import * as mock from "./mock-client";

const useMock = process.env.NEXT_PUBLIC_USE_MOCK_AUTH === "true";
const impl = useMock ? mock : real;

export const login = impl.login;
export const signup = impl.signup;
export const logout = impl.logout;

export type { AuthPayload, AuthResponse } from "./client";
