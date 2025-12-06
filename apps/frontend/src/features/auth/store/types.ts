import type { AuthUser } from '../api/types';

export type AuthStatus = 'idle' | 'loading' | 'authenticated' | 'unauthenticated';

export type AuthState = {
  user: AuthUser | null;
  needsVerification: boolean;
  status: AuthStatus;
  error: string | null;
  errorStatus: number | null;
};
