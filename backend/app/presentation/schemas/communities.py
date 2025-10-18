from typing import List, Optional

from pydantic import BaseModel
from .users import UserOut


class CommunityCreateIn(BaseModel):
    name: str
    company_id: Optional[str] = None
    tags: List[str] = []
    description: Optional[str] = None
    telegram_url: Optional[str] = None


class CommunityUpdateIn(BaseModel):
    name: Optional[str] = None
    tags: Optional[List[str]] = None
    description: Optional[str] = None
    telegram_url: Optional[str] = None


class CommunityOut(BaseModel):
    id: str
    name: str
    company_id: Optional[str]
    description: Optional[str] = None
    telegram_url: Optional[str] = None
    tags: List[str]
    is_archived: bool


class CommunityWithMembersOut(CommunityOut):
    members: List[UserOut] = []
