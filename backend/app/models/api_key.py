import uuid
from sqlalchemy import Column, String, Boolean, DateTime, func, UUID, ForeignKey, Text, Integer
from sqlalchemy.orm import relationship
from .base import Base

class ApiKey(Base):
    __tablename__ = "api_keys"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    encrypted_key = Column(Text, nullable=False)
    key_name = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)

    quota_limit = Column(Integer, nullable=True)
    quota_used = Column(Integer, default=0)

    last_used_at = Column(DateTime(timezone=True), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="api_keys")
    sessions = relationship("Session", back_populates="api_key")