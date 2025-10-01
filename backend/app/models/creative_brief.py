import uuid
from sqlalchemy import Column, String, DateTime, func, UUID, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from .base import Base

class CreativeBrief(Base):
    __tablename__ = "creative_briefs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)

    core_idea = Column(Text, nullable=False)
    genre = Column(String(100), nullable=False)
    target_audience = Column(Text, nullable=True)

    main_characters = Column(JSONB, default=[])
    themes = Column(JSONB, default=[])
    constraints = Column(JSONB, default={})
    preferences = Column(JSONB, default={})

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    session = relationship("Session", back_populates="creative_brief")