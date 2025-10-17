from pydantic import BaseModel
from typing import Optional, List

class MediaOut(BaseModel):
    id: str
    kind: str
    mime: str
    ext: Optional[str] = None
    size: int
    url: str

class PostCreateIn(BaseModel):
    community_id: str
    title: str
    body: str
    featured: bool = False
    media_uids: List[str] = []   # NEW — список uid медиа

class PostUpdateIn(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    featured: Optional[bool] = None
    media_uids: Optional[List[str]] = None  # NEW — можно заменить медиа

class PostOut(BaseModel):
    id: str
    community_id: str
    author_user_id: str
    title: str
    body: str
    featured: bool
    media: List[MediaOut] = []   # NEW

class StoryCreateIn(BaseModel):
    community_id: str
    title: str
    media_uid: str               # NEW — одна фотка/видео

class StoryOut(BaseModel):
    id: str
    community_id: str
    title: str
    media_url: str
    media: Optional[MediaOut] = None  # NEW