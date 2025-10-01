import uuid
from sqlalchemy import Column, String, DateTime, func, UUID, ForeignKey, Text, Integer, DECIMAL, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from .base import Base

class Agent(Base):
    __tablename__ = "agents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False, index=True)

    agent_type = Column(String(50), nullable=False, index=True)
    agent_name = Column(String(100), nullable=False)
    guide_content = Column(Text, nullable=True)

    model_name = Column(String(50), default="gemini-2.5-pro")
    temperature = Column(DECIMAL(3, 2), default=0.70)
    max_tokens = Column(Integer, default=40000)

    status = Column(String(50), default="initialized")
    is_active = Column(Boolean, default=True)

    config = Column(JSONB, default={})
    statistics = Column(JSONB, default={})

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("Session", back_populates="agents")
    reviews = relationship("Review", back_populates="agent", cascade="all, delete-orphan")