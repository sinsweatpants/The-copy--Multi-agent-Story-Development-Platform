import uuid
from typing import List, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class IdeaBase(BaseModel):
    title: str
    logline: str
    synopsis: str
    three_act_structure: Dict[str, Any]
    main_characters: List[Dict[str, Any]]
    key_scenes: List[Dict[str, Any]]
    thematic_elements: List[str]
    unique_selling_points: List[str]

class IdeaCreate(IdeaBase):
    session_id: uuid.UUID
    idea_number: int
    generated_by_agents: List[str]

class Idea(IdeaBase):
    id: uuid.UUID
    session_id: uuid.UUID
    idea_number: int
    generated_at: datetime

    class Config:
        from_attributes = True