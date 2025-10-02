import uuid
from typing import List
from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

class ReviewBase(BaseModel):
    quality_score: Decimal
    novelty_score: Decimal
    impact_score: Decimal
    quality_analysis: str
    novelty_analysis: str
    impact_analysis: str
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]
    overall_verdict: str

class ReviewCreate(ReviewBase):
    session_id: uuid.UUID
    agent_id: uuid.UUID
    idea_id: uuid.UUID

class Review(ReviewBase):
    id: uuid.UUID
    session_id: uuid.UUID
    agent_id: uuid.UUID
    idea_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True