import uuid
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime

# Schema for a single argument made by an agent in a turn
class Argument(BaseModel):
    agent_name: str
    supporting_idea: int  # 1 or 2
    strengths_highlighted: List[str]
    weaknesses_criticized: List[str]
    comparative_points: List[str]
    specialized_insight: str
    evidence_from_review: List[str]
    rebuttal_to_previous: Optional[str] = None

# Schema for a single turn in the tournament
class TournamentTurn(BaseModel):
    turn_number: int
    participants: List[str]
    arguments: List[Argument]
    timestamp: datetime

# Base schema for the tournament itself
class TournamentBase(BaseModel):
    status: str = "active"
    current_turn: int = 0
    max_turns: int = 8

class TournamentCreate(BaseModel):
    session_id: uuid.UUID

class TournamentUpdate(BaseModel):
    status: Optional[str] = None
    current_turn: Optional[int] = None

class Tournament(TournamentBase):
    id: uuid.UUID
    session_id: uuid.UUID
    started_at: datetime
    ended_at: Optional[datetime] = None
    turns: List[TournamentTurn] = [] # This can be populated from the related turns table

    class Config:
        from_attributes = True