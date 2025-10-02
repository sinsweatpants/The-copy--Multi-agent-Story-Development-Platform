import uuid
from typing import Optional, Dict, Any
from pydantic import BaseModel
from decimal import Decimal

class AgentBase(BaseModel):
    agent_type: str
    agent_name: str
    model_name: Optional[str] = "gemini-2.5-pro"
    temperature: Optional[Decimal] = 0.70
    max_tokens: Optional[int] = 40000
    config: Optional[Dict[str, Any]] = {}

class AgentCreate(AgentBase):
    session_id: uuid.UUID

class AgentUpdate(BaseModel):
    status: Optional[str] = None
    is_active: Optional[bool] = None

class Agent(AgentBase):
    id: uuid.UUID
    session_id: uuid.UUID
    status: str
    is_active: bool

    class Config:
        from_attributes = True