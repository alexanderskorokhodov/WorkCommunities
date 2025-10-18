from typing import Optional

from pydantic import BaseModel


class CompanyCreateIn(BaseModel):
    name: str
    description: Optional[str] = None
    tags: Optional[list[str]] = None


class CompanyUpdateIn(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    logo_media_id: Optional[str] = None
    tags: Optional[list[str]] = None


class CompanyOut(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    logo_media_id: Optional[str] = None
    tags: list[str] = []
