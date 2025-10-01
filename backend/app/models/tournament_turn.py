import uuid
from sqlalchemy import Column, DateTime, func, UUID, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from .base import Base

class TournamentTurn(Base):
    __tablename__ = "tournament_turns"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tournament_id = Column(UUID(as_uuid=True), ForeignKey("tournaments.id", ondelete="CASCADE"), nullable=False, index=True)
    turn_number = Column(Integer, nullable=False, index=True)

    participating_agents = Column(JSONB, nullable=False)
    arguments = Column(JSONB, nullable=False, default=[])

    turn_metadata = Column(JSONB, default={})

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    tournament = relationship("Tournament", back_populates="turns")