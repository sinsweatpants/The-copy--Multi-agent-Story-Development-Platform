import uuid
from sqlalchemy import Column, String, DateTime, func, UUID, ForeignKey, Text, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from .base import Base

class Idea(Base):
    __tablename__ = "ideas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    idea_number = Column(Integer, nullable=False) # 1 or 2

    title = Column(String(255), nullable=False)
    logline = Column(Text, nullable=False)
    synopsis = Column(Text, nullable=False)

    three_act_structure = Column(JSONB, nullable=False)
    main_characters = Column(JSONB, nullable=False, default=[])
    key_scenes = Column(JSONB, nullable=False, default=[])
    thematic_elements = Column(JSONB, default=[])
    unique_selling_points = Column(JSONB, default=[])

    generated_by_agents = Column(JSONB, nullable=False)
    generation_metadata = Column(JSONB, default={})

    generated_at = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("Session", back_populates="ideas")
    reviews = relationship("Review", back_populates="idea", cascade="all, delete-orphan")
    winning_decision = relationship("FinalDecision", foreign_keys="[FinalDecision.winning_idea_id]", back_populates="winning_idea", cascade="all, delete-orphan")
    losing_decision = relationship("FinalDecision", foreign_keys="[FinalDecision.losing_idea_id]", back_populates="losing_idea", cascade="all, delete-orphan")