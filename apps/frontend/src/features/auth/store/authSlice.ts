import { createSlice } from '@reduxjs/toolkit';
import type { AuthStatus, AuthState } from './types';
import {
  login,
  signup,
  logout,
  resendVerification,
  verifyEmail,
  refresh,
  me,
} from './thunks';

const initialState: AuthState = {
  user: null,
  needsVerification: false,
  status: 'idle',
  error: null,
  errorStatus: null,
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(login.pending, (state) => {
        state.status = 'loading';
        state.error = null;
        state.errorStatus = null;
      })
      .addCase(login.fulfilled, (state, action) => {
        state.status = 'authenticated';
        state.user = action.payload.user;
        state.needsVerification = !!action.payload.needsVerification;
        state.error = null;
        state.errorStatus = null;
      })
      .addCase(login.rejected, (state, action) => {
        state.status = 'unauthenticated';
        state.error =
          (action.payload as any)?.message ??
          action.error.message ??
          'Login failed';
        state.errorStatus = (action.payload as any)?.status ?? null;
      })
      .addCase(signup.pending, (state) => {
        state.status = 'loading';
        state.error = null;
        state.errorStatus = null;
      })
      .addCase(signup.fulfilled, (state, action) => {
        state.status = 'authenticated';
        state.user = action.payload.user;
        state.needsVerification = !!action.payload.needsVerification;
        state.error = null;
        state.errorStatus = null;
      })
      .addCase(signup.rejected, (state, action) => {
        state.status = 'unauthenticated';
        state.error =
          (action.payload as any)?.message ??
          action.error.message ??
          'Signup failed';
        state.errorStatus = (action.payload as any)?.status ?? null;
      })
      .addCase(logout.pending, (state) => {
        state.error = null;
        state.errorStatus = null;
      })
      .addCase(logout.fulfilled, (state) => {
        state.status = 'unauthenticated';
        state.user = null;
        state.needsVerification = false;
        state.error = null;
        state.errorStatus = null;
      })
      .addCase(logout.rejected, (state, action) => {
        state.error =
          (action.payload as any)?.message ??
          action.error.message ??
          'Logout failed';
        state.errorStatus = (action.payload as any)?.status ?? null;
      })
      .addCase(resendVerification.pending, (state) => {
        state.error = null;
        state.errorStatus = null;
      })
      .addCase(resendVerification.rejected, (state, action) => {
        state.error =
          (action.payload as any)?.message ??
          action.error.message ??
          'Resend verification failed';
        state.errorStatus = (action.payload as any)?.status ?? null;
      })
      .addCase(verifyEmail.pending, (state) => {
        state.error = null;
        state.errorStatus = null;
      })
      .addCase(verifyEmail.fulfilled, (state, action) => {
        state.status = 'authenticated';
        state.user = action.payload.user;
        state.needsVerification = false;
        state.error = null;
        state.errorStatus = null;
      })
      .addCase(verifyEmail.rejected, (state, action) => {
        state.error =
          (action.payload as any)?.message ??
          action.error.message ??
          'Email verification failed';
        state.errorStatus = (action.payload as any)?.status ?? null;
      })
      .addCase(me.pending, (state) => {
        state.status = 'loading';
        state.error = null;
        state.errorStatus = null;
      })
      .addCase(me.fulfilled, (state, action) => {
        state.status = 'authenticated';
        state.user = action.payload.user;
        state.needsVerification = !!action.payload.needsVerification;
        state.error = null;
        state.errorStatus = null;
      })
      .addCase(me.rejected, (state, action) => {
        state.status = 'unauthenticated';
        state.user = null;
        state.needsVerification = false;
        state.error =
          (action.payload as any)?.message ??
          action.error.message ??
          'Session check failed';
        state.errorStatus = (action.payload as any)?.status ?? null;
      })
      .addCase(refresh.pending, (state) => {
        state.error = null;
        state.errorStatus = null;
      })
      .addCase(refresh.fulfilled, (state, action) => {
        state.status = 'authenticated';
        state.user = action.payload.user;
        state.needsVerification = !!action.payload.needsVerification;
        state.error = null;
        state.errorStatus = null;
      })
      .addCase(refresh.rejected, (state, action) => {
        state.status = 'unauthenticated';
        state.user = null;
        state.needsVerification = false;
        state.error =
          (action.payload as any)?.message ??
          action.error.message ??
          'Session refresh failed';
        state.errorStatus = (action.payload as any)?.status ?? null;
      });
  },
});

export default authSlice.reducer;
