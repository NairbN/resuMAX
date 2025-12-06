import { createAsyncThunk } from '@reduxjs/toolkit';
import {
  login as loginApi,
  signup as signupApi,
  logout as logoutApi,
  resendVerification as resendVerificationApi,
  verifyEmail as verifyEmailApi,
  refresh as refreshApi,
  me as meApi,
} from '@/features/auth/api';
import type { AuthResponse } from '@/features/auth/api';

type RejectPayload = { message: string; status?: number };

const formatError = (err: any, fallback: string): RejectPayload => ({
  message: err?.message ?? fallback,
  status: err?.status,
});

export const login = createAsyncThunk<
  AuthResponse,
  { email: string; password: string },
  { rejectValue: RejectPayload }
>('auth/login', async (payload, { rejectWithValue }) => {
  try {
    return await loginApi(payload);
  } catch (err) {
    return rejectWithValue(formatError(err, 'Login failed'));
  }
});

export const signup = createAsyncThunk<
  AuthResponse,
  { email: string; password: string },
  { rejectValue: RejectPayload }
>('auth/signup', async (payload, { rejectWithValue }) => {
  try {
    return await signupApi(payload);
  } catch (err) {
    return rejectWithValue(formatError(err, 'Signup failed'));
  }
});

export const logout = createAsyncThunk<void, void, { rejectValue: RejectPayload }>(
  'auth/logout',
  async (_, { rejectWithValue }) => {
    try {
      await logoutApi();
    } catch (err) {
      return rejectWithValue(formatError(err, 'Logout failed'));
    }
  },
);

export const resendVerification = createAsyncThunk<
  void,
  void,
  { rejectValue: RejectPayload }
>('auth/resendVerification', async (_, { rejectWithValue }) => {
  try {
    await resendVerificationApi();
  } catch (err) {
    return rejectWithValue(formatError(err, 'Resend verification failed'));
  }
});

export const verifyEmail = createAsyncThunk<
  AuthResponse,
  string,
  { rejectValue: RejectPayload }
>('auth/verifyEmail', async (token, { rejectWithValue }) => {
  try {
    return await verifyEmailApi(token);
  } catch (err) {
    return rejectWithValue(formatError(err, 'Email verification failed'));
  }
});

export const me = createAsyncThunk<AuthResponse, void, { rejectValue: RejectPayload }>(
  'auth/me',
  async (_, { rejectWithValue }) => {
    try {
      return await meApi();
    } catch (err) {
      return rejectWithValue(formatError(err, 'Session check failed'));
    }
  },
);

export const refresh = createAsyncThunk<
  AuthResponse,
  void,
  { rejectValue: RejectPayload }
>('auth/refresh', async (_, { rejectWithValue }) => {
  try {
    return await refreshApi();
  } catch (err) {
    return rejectWithValue(formatError(err, 'Session refresh failed'));
  }
});
