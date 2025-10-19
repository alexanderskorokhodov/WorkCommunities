from datetime import datetime
from typing import Optional

from pydantic import BaseModel, root_validator


class CaseCreateIn(BaseModel):
    title: str
    description: Optional[str] = None
    date: datetime
    solutions_count: int = 0


class CaseOut(BaseModel):
    id: str
    community_id: str
    title: str
    description: Optional[str] = None
    date: datetime
    solutions_count: int

    @root_validator(pre=True)
    def _fill_nulls(cls, values: dict):
        if values.get("description") is None:
            values["description"] = ""
        return values
