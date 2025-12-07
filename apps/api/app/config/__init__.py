import os
from datetime import timedelta
from pydantic import BaseModel, Field


class Settings(BaseModel):
    jwt_secret: str = Field(default=os.getenv("AUTH_SECRET", "dev-secret"))
    access_expires: timedelta = Field(default=timedelta(minutes=15))
    refresh_expires: timedelta = Field(default=timedelta(days=30))
    database_url: str = Field(default=os.getenv("DATABASE_URL", "sqlite:///./dev.db"))
    allowed_origins: list[str] = Field(
        default_factory=lambda: os.getenv("FRONTEND_ORIGINS", "http://localhost:3000").split(",")
    )

    cookie_domain: str | None = Field(default=os.getenv("COOKIE_DOMAIN"))
    cookie_secure: bool = Field(default=os.getenv("COOKIE_SECURE", "false").lower() == "true")
    cookie_samesite: str = Field(default=os.getenv("COOKIE_SAMESITE", "lax"))

    rate_limit_attempts: int = Field(default=int(os.getenv("RATE_LIMIT_ATTEMPTS", "5")))
    rate_limit_window_seconds: int = Field(default=int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "300")))

    verify_base_url: str | None = Field(default=os.getenv("VERIFY_BASE_URL"))
    auto_verify: bool = Field(default=os.getenv("AUTO_VERIFY", "true").lower() == "true")
    redis_url: str | None = Field(default=os.getenv("REDIS_URL"))
    smtp_host: str | None = Field(default=os.getenv("SMTP_HOST"))
    smtp_port: int | None = Field(default=int(os.getenv("SMTP_PORT", "0")) if os.getenv("SMTP_PORT") else None)
    smtp_user: str | None = Field(default=os.getenv("SMTP_USER"))
    smtp_password: str | None = Field(default=os.getenv("SMTP_PASSWORD"))
    smtp_tls: bool = Field(default=os.getenv("SMTP_TLS", "true").lower() == "true")


settings = Settings()
