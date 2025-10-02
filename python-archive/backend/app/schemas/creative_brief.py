import uuid
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class Character(BaseModel):
    name: str
    description: str

class CreativeBriefBase(BaseModel):
    core_idea: str = Field(..., min_length=50, max_length=5000)
    genre: str = Field(..., min_length=3, max_length=100)
    target_audience: Optional[str] = Field(None, max_length=1000)
    main_characters: List[Character] = []
    themes: List[str] = []
    constraints: Optional[Dict[str, Any]] = {}
    preferences: Optional[Dict[str, Any]] = {}

class CreativeBriefCreate(CreativeBriefBase):
    session_id: uuid.UUID

class CreativeBriefUpdate(CreativeBriefBase):
    pass

class CreativeBrief(CreativeBriefBase):
    id: uuid.UUID
    session_id: uuid.UUID

    class Config:
        from_attributes = True