from typing import Optional, List

from pydantic import BaseModel, AnyUrl
from app.presentation.schemas.communities import CommunityOut
from app.presentation.schemas.events import EventOut


class SphereOut(BaseModel):
    id: str
    title: str
    background_color: str
    text_color: str


class SkillOut(BaseModel):
    id: str
    title: str
    sphere: Optional[SphereOut] = None


class StatusOut(BaseModel):
    id: str
    title: str


class ProfileOut(BaseModel):
    id: str
    user_id: str
    full_name: Optional[str] = None
    portfolio_url: Optional[str] = None
    description: Optional[str] = None
    skills: List[SkillOut] = []
    statuses: List[StatusOut] = []
    communities: List[CommunityOut] = []
    joined_events: List[EventOut] = []


class ProfileUpdateIn(BaseModel):
    full_name: Optional[str] = None
    portfolio_url: Optional[str] = None
    description: Optional[str] = None
    skill_uids: Optional[List[str]] = None
    status_uids: Optional[List[str]] = None
