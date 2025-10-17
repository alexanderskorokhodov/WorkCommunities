from typing import Optional

from pydantic import BaseModel


class PostCreateIn(BaseModel):
    community_id: str
    title: str
    body: str
    featured: bool = False


class PostUpdateIn(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    featured: Optional[bool] = None


class PostOut(BaseModel):
    id: str
    community_id: str
    author_user_id: str
    title: str
    body: str
    featured: bool


class StoryCreateIn(BaseModel):
    community_id: str
    title: str
    media_url: str


class StoryOut(BaseModel):
    id: str
    community_id: str
    title: str
    media_url: str
