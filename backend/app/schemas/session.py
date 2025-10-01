import uuid
from typing import Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class SessionBase(BaseModel):
    metadata: Optional[Dict[str, Any]] = None

class SessionCreate(BaseModel):
    api_key_id: uuid.UUID

class SessionUpdate(BaseModel):
    status: Optional[str] = None
    current_phase: Optional[str] = None

class Session(SessionBase):
    id: uuid.UUID
    user_id: uuid.UUID
    api_key_id: uuid.UUID
    status: str
    current_phase: str
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True