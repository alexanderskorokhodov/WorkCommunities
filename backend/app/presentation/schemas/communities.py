from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel, root_validator
from .cases import CaseOut
from .users import UserOut


class CommunityCreateIn(BaseModel):
    name: str
    company_id: Optional[str] = None
    tags: List[str] = []
    description: Optional[str] = None
    telegram_url: Optional[str] = None
    logo_media_id: Optional[str] = None


class CommunityUpdateIn(BaseModel):
    name: Optional[str] = None
    tags: Optional[List[str]] = None
    description: Optional[str] = None
    telegram_url: Optional[str] = None
    logo_media_id: Optional[str] = None


class CommunityOut(BaseModel):
    id: str
    name: str
    company_id: Optional[str]
    description: Optional[str] = None
    telegram_url: Optional[str] = None
    tags: List[str]
    is_archived: bool
    logo_media_id: Optional[str] = None
    members_count: Optional[int] = None

    @root_validator(pre=True)
    def _fill_nulls(cls, values: dict):
        # convert nullables to presentation defaults
        for k in ("description", "telegram_url", "logo_media_id"):
            if values.get(k) is None:
                values[k] = ""
        if values.get("company_id") is None:
            values["company_id"] = ""
        if values.get("members_count") is None:
            values["members_count"] = 0
        return values


class CommunityWithMembersOut(CommunityOut):
    # Backward-compat alias not used by current endpoints; prefer CommunityDetailOut
    members: List[UserOut] = []


class CommunityMemberOut(BaseModel):
    id: str
    role: str
    phone: Optional[str] = None
    full_name: Optional[str] = None
    avatar_media_id: Optional[str] = None
    created_at: datetime

    @root_validator(pre=True)
    def _fill_nulls(cls, values: dict):
        for k in ("phone", "full_name", "avatar_media_id"):
            if values.get(k) is None:
                values[k] = ""
        return values


class CommunityDetailOut(CommunityOut):
    cases: List[CaseOut] = []
    # Members list for community detail: expose full_name, omit email
    members: List[CommunityMemberOut] = []
