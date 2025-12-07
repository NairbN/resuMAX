import datetime as dt
import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Index
from sqlalchemy.orm import relationship

from app.db.session import Base
from app.models.user import _utcnow


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    token = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), default=_utcnow, nullable=False)

    user = relationship("User", back_populates="refresh_tokens")


Index("ix_refresh_user_id", RefreshToken.user_id)
