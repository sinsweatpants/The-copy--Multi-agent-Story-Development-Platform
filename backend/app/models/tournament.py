import uuid
from sqlalchemy import Column, String, DateTime, func, UUID, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from .base import Base

class Tournament(Base):
    __tablename__ = "tournaments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)

    status = Column(String(50), nullable=False, default="active")
    current_turn = Column(Integer, default=0)
    max_turns = Column(Integer, default=8)

    tournament_data = Column(JSONB, default={})

    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True)

    session = relationship("Session", back_populates="tournament")
    turns = relationship("TournamentTurn", back_populates="tournament", cascade="all, delete-orphan")
    final_decision = relationship("FinalDecision", back_populates="tournament", uselist=False, cascade="all, delete-orphan")