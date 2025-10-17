from typing import List, Optional

from pydantic import BaseModel


class CommunityCreateIn(BaseModel):
    name: str
    company_id: Optional[str] = None
    tags: List[str] = []


class CommunityUpdateIn(BaseModel):
    name: Optional[str] = None
    tags: Optional[List[str]] = None


class CommunityOut(BaseModel):
    id: str
    name: str
    company_id: Optional[str]
    tags: List[str]
    is_archived: bool
