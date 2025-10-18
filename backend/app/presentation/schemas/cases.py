from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CaseCreateIn(BaseModel):
    title: str
    description: Optional[str] = None
    date: datetime
    points: int = 0


class CaseOut(BaseModel):
    id: str
    community_id: str
    title: str
    description: Optional[str] = None
    date: datetime
    points: int

