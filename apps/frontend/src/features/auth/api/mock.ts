import type { AuthResponse } from './types';

type Credentials = { email: string; password: string };

const sleep = (ms = 300) => new Promise((resolve) => setTimeout(resolve, ms));

let mockUser = {
  id: 'user_123',
  email: 'mockuser@example.com',
  password: 'password123',
  verified: false,
};

let loggedIn = false;

const authResponse = (): AuthResponse => ({
  token: 'mock-token',
  user: {
    id: mockUser.id,
    email: mockUser.email,
    verified: mockUser.verified,
  },
  needsVerification: !mockUser.verified,
});

const throwError = (status: number, message: string): never => {
  throw { status, message };
};

export async function signup(payload: Credentials): Promise<AuthResponse> {
  await sleep();
  mockUser = {
    id: mockUser.id,
    email: payload.email,
    password: payload.password,
    verified: false,
  };
  loggedIn = true;
  return authResponse();
}

export function setMockVerification(verified: boolean) {
  mockUser.verified = verified;
}

export async function login(payload: Credentials): Promise<AuthResponse> {
  await sleep();

  if (payload.email !== mockUser.email || payload.password !== mockUser.password) {
    throwError(401, 'Invalid credentials');
  }

  loggedIn = true;
  return authResponse();
}

export async function logout(): Promise<void> {
  await sleep(150);
  loggedIn = false;
}

export async function resendVerification(): Promise<void> {
  await sleep(200);
}

export async function verifyEmail(token: string): Promise<AuthResponse> {
  await sleep();

  if (!token) {
    throwError(400, 'Missing token');
  }

  mockUser.verified = true;
  loggedIn = true;
  return authResponse();
}

export async function me(): Promise<AuthResponse> {
  await sleep(150);

  if (!loggedIn) {
    throwError(401, 'Not authenticated');
  }

  return authResponse();
}

export async function refresh(): Promise<AuthResponse> {
  await sleep(150);

  if (!loggedIn) {
    throwError(401, 'Not authenticated');
  }

  return authResponse();
}
