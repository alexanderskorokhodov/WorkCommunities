from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, root_validator


class CommunityForUserOut(BaseModel):
    id: str
    name: str
    company_id: Optional[str]
    description: Optional[str] = None
    telegram_url: Optional[str] = None
    tags: List[str]
    is_archived: bool
    logo_media_id: Optional[str] = None

    @root_validator(pre=True)
    def _fill_nulls(cls, values: dict):
        if values.get("company_id") is None:
            values["company_id"] = ""
        for k in ("description", "telegram_url", "logo_media_id"):
            if values.get(k) is None:
                values[k] = ""
        return values


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

    @root_validator(pre=True)
    def _fill_nulls(cls, values: dict):
        for k in ("phone", "email", "avatar_media_id"):
            if values.get(k) is None:
                values[k] = ""
        return values


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

    @root_validator(pre=True)
    def _fill_nulls(cls, values: dict):
        for k in ("phone", "full_name", "portfolio_url", "description", "avatar_media_id"):
            if values.get(k) is None:
                values[k] = ""
        return values
