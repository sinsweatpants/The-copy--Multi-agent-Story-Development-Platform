import uuid
from typing import List, Dict
from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

class FinalDecisionBase(BaseModel):
    winning_idea_id: uuid.UUID
    losing_idea_id: uuid.UUID
    decision_rationale: str
    key_strengths: List[str]
    addressed_weaknesses: List[str]
    vote_breakdown: Dict[str, int]
    unanimous: bool
    confidence_score: Decimal
    implementation_recommendations: List[str]
    next_steps: List[str]

class FinalDecisionCreate(FinalDecisionBase):
    session_id: uuid.UUID
    tournament_id: uuid.UUID

class FinalDecision(FinalDecisionBase):
    id: uuid.UUID
    session_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True