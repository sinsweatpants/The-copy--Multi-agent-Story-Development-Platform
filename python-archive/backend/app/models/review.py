import uuid
from sqlalchemy import Column, DateTime, func, UUID, ForeignKey, Text, DECIMAL
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from .base import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="CASCADE"), nullable=False, index=True)
    idea_id = Column(UUID(as_uuid=True), ForeignKey("ideas.id", ondelete="CASCADE"), nullable=False, index=True)

    quality_score = Column(DECIMAL(3, 1), nullable=False)
    novelty_score = Column(DECIMAL(3, 1), nullable=False)
    impact_score = Column(DECIMAL(3, 1), nullable=False)

    quality_analysis = Column(Text, nullable=False)
    novelty_analysis = Column(Text, nullable=False)
    impact_analysis = Column(Text, nullable=False)

    strengths = Column(JSONB, default=[])
    weaknesses = Column(JSONB, default=[])
    recommendations = Column(JSONB, default=[])

    overall_verdict = Column(Text, nullable=False)

    review_metadata = Column(JSONB, default={})

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("Session", back_populates="reviews")
    agent = relationship("Agent", back_populates="reviews")
    idea = relationship("Idea", back_populates="reviews")