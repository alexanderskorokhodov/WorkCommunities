from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel
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


class CommunityDetailOut(CommunityOut):
    cases: List[CaseOut] = []
    # Members list for community detail: expose full_name, omit email
    members: List[CommunityMemberOut] = []
