from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel
from app.presentation.schemas.content import SkillOut


class EventOut(BaseModel):
    id: str
    community_id: str
    title: str
    event_date: datetime
    city: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    registration: Optional[str] = None
    format: Optional[str] = None
    media_id: Optional[str] = None
    tags: List[str] = []
    skills: List[SkillOut] = []
    cost: Optional[int] = None
    participant_payout: Optional[int] = None


class EventCreateIn(BaseModel):
    community_id: str
    title: str
    event_date: datetime
    city: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    registration: Optional[str] = None
    format: Optional[str] = None
    media_id: Optional[str] = None
    tags: Optional[List[str]] = None
    skill_ids: Optional[List[str]] = None
    cost: Optional[int] = None
    participant_payout: Optional[int] = None
