import { api } from '@/services/api/client';
import { getError } from '@/services/api/errors';
import * as mock from './mock';
import type { AuthResponse } from './types';

const useMock = process.env.NEXT_PUBLIC_USE_AUTH_MOCK === 'true';

export async function login(payload: { email: string; password: string }): Promise<AuthResponse> {
  if (useMock) {
    return mock.login(payload);
  }
  try {
    const response = await api.post<AuthResponse>('/auth/login', payload);
    return response.data;
  } catch (err) {
    throw getError(err);
  }
}

export async function signup(payload: { email: string; password: string }): Promise<AuthResponse> {
  if (useMock) {
    return mock.signup(payload);
  }
  try {
    const response = await api.post<AuthResponse>('/auth/signup', payload);
    return response.data;
  } catch (err) {
    throw getError(err);
  }
}

export async function logout(){
    if (useMock) {
      return mock.logout();
    }
    try {
        await api.post('/auth/logout');
    } catch (err) {
        throw getError(err);
    }
}

export async function resendVerification(){
    if (useMock) {
      return mock.resendVerification();
    }
    try {
        await api.post('/auth/resend-verification');
    } catch (err) {
        throw getError(err);
    }
}

export async function verifyEmail(token: string){
    if (useMock) {
      return mock.verifyEmail(token);
    }
    try {
        const { data } = await api.post<AuthResponse>('/auth/verify-email', { token });
        return data;
    } catch (err) {
        throw getError(err);
    }
}

export async function me(){
    if (useMock) {
      return mock.me();
    }
    try {
        const { data } = await api.get<AuthResponse>('/auth/me');
        return data;
    } catch (err) {
        throw getError(err);
    }
}

export async function refresh(){
    if (useMock) {
      return mock.refresh();
    }
    try {
        const { data } = await api.post<AuthResponse>('/auth/refresh');
        return data;
    } catch (err) {
        throw getError(err);
    }
}

export type { AuthResponse } from './types';
