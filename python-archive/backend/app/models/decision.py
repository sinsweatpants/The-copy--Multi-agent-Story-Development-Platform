import uuid
from sqlalchemy import Column, String, DateTime, func, UUID, ForeignKey, Text, Boolean, DECIMAL
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from .base import Base

class FinalDecision(Base):
    __tablename__ = "final_decisions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    tournament_id = Column(UUID(as_uuid=True), ForeignKey("tournaments.id"), nullable=False)

    winning_idea_id = Column(UUID(as_uuid=True), ForeignKey("ideas.id"), nullable=False)
    losing_idea_id = Column(UUID(as_uuid=True), ForeignKey("ideas.id"), nullable=False)

    decision_rationale = Column(Text, nullable=False)
    key_strengths = Column(JSONB, default=[])
    addressed_weaknesses = Column(JSONB, default=[])

    vote_breakdown = Column(JSONB, nullable=False)
    unanimous = Column(Boolean, nullable=False)
    confidence_score = Column(DECIMAL(3, 2))

    implementation_recommendations = Column(JSONB, default=[])
    next_steps = Column(JSONB, default=[])

    decision_metadata = Column(JSONB, default={})

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("Session", back_populates="final_decision")
    tournament = relationship("Tournament", back_populates="final_decision")
    winning_idea = relationship("Idea", foreign_keys=[winning_idea_id], back_populates="winning_decision")
    losing_idea = relationship("Idea", foreign_keys=[losing_idea_id], back_populates="losing_decision")