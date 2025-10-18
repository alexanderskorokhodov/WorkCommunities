from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserOut(BaseModel):
    id: str
    role: str
    phone: Optional[str] = None
    email: Optional[str] = None
    created_at: datetime

