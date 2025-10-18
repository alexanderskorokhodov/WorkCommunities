from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class EventOut(BaseModel):
    id: str
    community_id: str
    title: str
    starts_at: datetime
    city: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    registration: Optional[str] = None
    format: Optional[str] = None
    media_id: Optional[str] = None


class EventCreateIn(BaseModel):
    community_id: str
    title: str
    starts_at: datetime
    city: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    registration: Optional[str] = None
    format: Optional[str] = None
    media_id: Optional[str] = None
