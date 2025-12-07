from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class AuthUser(BaseModel):
  id: str
  email: EmailStr
  verified: bool = False


class AuthResponse(BaseModel):
  token: Optional[str] = None
  user: AuthUser
  needsVerification: bool = False


class SignupRequest(BaseModel):
  email: EmailStr
  password: str = Field(min_length=8)


class LoginRequest(BaseModel):
  email: EmailStr
  password: str


class VerifyRequest(BaseModel):
  token: str


class ResendRequest(BaseModel):
  email: EmailStr
