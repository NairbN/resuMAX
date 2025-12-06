export type AuthUser = {
  id: string;
  email: string;
  verified?: boolean;
};

export type AuthResponse = {
  token?: string;
  user: AuthUser;
  needsVerification?: boolean;
};
