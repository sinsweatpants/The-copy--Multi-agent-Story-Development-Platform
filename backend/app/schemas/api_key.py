import uuid
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class ApiKeyBase(BaseModel):
    key_name: Optional[str] = None

class ApiKeyCreate(ApiKeyBase):
    api_key: str # The raw key, to be encrypted by the service

class ApiKeyUpdate(ApiKeyBase):
    is_active: Optional[bool] = None

class ApiKey(ApiKeyBase):
    id: uuid.UUID
    user_id: uuid.UUID
    is_active: bool
    last_used_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True