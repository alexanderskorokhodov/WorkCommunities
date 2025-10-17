from typing import Optional, List

from pydantic import BaseModel


class ProfileCreateIn(BaseModel):
    full_name: Optional[str] = None
    city: Optional[str] = None
    interests: List[str] = []


class ProfileOut(ProfileCreateIn):
    id: str
    user_id: str
