from typing import Optional

from pydantic import BaseModel, root_validator
from app.presentation.schemas.content import MediaOut, SkillOut
from .communities import CommunityOut


class CompanyCreateIn(BaseModel):
    name: str
    description: Optional[str] = None
    tags: Optional[list[str]] = None


class CompanyUpdateIn(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    logo_media_id: Optional[str] = None
    tags: Optional[list[str]] = None
    media_uids: Optional[list[str]] = None  # additional media for company


class CompanyOut(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    logo_media_id: Optional[str] = None
    skills: list[SkillOut] = []

    @root_validator(pre=True)
    def _fill_nulls(cls, values: dict):
        for k in ("description", "logo_media_id"):
            if values.get(k) is None:
                values[k] = ""
        return values


class CompanyDetailOut(CompanyOut):
    communities: list[CommunityOut] = []
    media: list[MediaOut] = []
