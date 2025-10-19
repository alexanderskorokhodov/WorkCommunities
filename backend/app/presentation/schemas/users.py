from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class CommunityForUserOut(BaseModel):
    id: str
    name: str
    company_id: Optional[str]
    description: Optional[str] = None
    telegram_url: Optional[str] = None
    tags: List[str]
    is_archived: bool
    logo_media_id: Optional[str] = None


class SphereForUserOut(BaseModel):
    id: str
    title: str
    background_color: str
    text_color: str


class SkillForUserOut(BaseModel):
    id: str
    title: str
    sphere: Optional[SphereForUserOut] = None


class StatusForUserOut(BaseModel):
    id: str
    title: str


class UserOut(BaseModel):
    id: str
    role: str
    phone: Optional[str] = None
    email: Optional[str] = None
    avatar_media_id: Optional[str] = None
    created_at: datetime


class UserDetailOut(BaseModel):
    id: str
    role: str
    phone: Optional[str] = None
    full_name: Optional[str] = None
    portfolio_url: Optional[str] = None
    description: Optional[str] = None
    skills: List[SkillForUserOut] = []
    statuses: List[StatusForUserOut] = []
    avatar_media_id: Optional[str] = None
    created_at: datetime
    communities: List[CommunityForUserOut] = []
