import uuid
from sqlalchemy import Column, String, DateTime, func, UUID, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from .base import Base

class Session(Base):
    __tablename__ = "sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    api_key_id = Column(UUID(as_uuid=True), ForeignKey("api_keys.id"), nullable=False)

    status = Column(String(50), nullable=False, default="initialized", index=True)
    current_phase = Column(String(50), nullable=False, default="brief")

    session_data = Column(JSONB, nullable=False, default={})

    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    metadata = Column(JSONB, default={})

    user = relationship("User", back_populates="sessions")
    api_key = relationship("ApiKey", back_populates="sessions")

    agents = relationship("Agent", back_populates="session", cascade="all, delete-orphan")
    creative_brief = relationship("CreativeBrief", back_populates="session", uselist=False, cascade="all, delete-orphan")
    ideas = relationship("Idea", back_populates="session", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="session", cascade="all, delete-orphan")
    tournament = relationship("Tournament", back_populates="session", uselist=False, cascade="all, delete-orphan")
    final_decision = relationship("FinalDecision", back_populates="session", uselist=False, cascade="all, delete-orphan")
    activity_logs = relationship("ActivityLog", back_populates="session", cascade="all, delete-orphan")