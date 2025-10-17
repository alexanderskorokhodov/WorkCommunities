
from pydantic import BaseModel
from typing import Optional, List

class ProfileCreateIn(BaseModel):
    full_name: Optional[str] = None
    city: Optional[str] = None
    interests: List[str] = []

class ProfileOut(ProfileCreateIn):
    id: str
    user_id: str
