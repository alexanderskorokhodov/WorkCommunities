from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel, root_validator


class MediaOut(BaseModel):
    id: str
    kind: str
    mime: str
    ext: Optional[str] = None
    size: int
    url: str

    @root_validator(pre=True)
    def _fill_nulls_media(cls, values: dict):
        if values.get("ext") is None:
            values["ext"] = ""
        return values


class ContentSphereOut(BaseModel):
    id: str
    title: str
    background_color: str
    text_color: str


class SkillOut(BaseModel):
    id: str
    title: str
    sphere_id: str
    sphere: Optional[ContentSphereOut] = None


class PostCreateIn(BaseModel):
    community_id: str
    title: str
    body: str
    media_uids: List[str] = []  # NEW — список uid медиа
    tags: Optional[List[str]] = None
    skill_ids: Optional[List[str]] = None
    cost: Optional[int] = None
    participant_payout: Optional[int] = None


class PostUpdateIn(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    media_uids: Optional[List[str]] = None  # NEW — можно заменить медиа
    tags: Optional[List[str]] = None
    skill_ids: Optional[List[str]] = None
    cost: Optional[int] = None
    participant_payout: Optional[int] = None


class PostOut(BaseModel):
    id: str
    community_id: str
    title: str
    body: str
    media: List[MediaOut] = []  # NEW
    tags: List[str] = []
    skills: List[SkillOut] = []
    cost: Optional[int] = None
    participant_payout: Optional[int] = None

    @root_validator(pre=True)
    def _fill_nulls_post(cls, values: dict):
        # body could be optional in other paths; ensure empty string
        if values.get("body") is None:
            values["body"] = ""
        if values.get("cost") is None:
            values["cost"] = 0
        if values.get("participant_payout") is None:
            values["participant_payout"] = 0
        return values


class ContentItemOut(BaseModel):
    id: str
    community_id: str
    type: str  # 'post' | 'event'
    title: str
    body: Optional[str] = None
    event_date: Optional[datetime] = None
    media: List[MediaOut] = []
    tags: List[str] = []
    skills: List[SkillOut] = []
    cost: Optional[int] = None
    participant_payout: Optional[int] = None

    @root_validator(pre=True)
    def _fill_nulls_item(cls, values: dict):
        if values.get("body") is None:
            values["body"] = ""
        if values.get("cost") is None:
            values["cost"] = 0
        if values.get("participant_payout") is None:
            values["participant_payout"] = 0
        return values


class StoryCreateIn(BaseModel):
    company_id: str
    title: str
    media_uid: str  # NEW — одна фотка/видео


class StoryOut(BaseModel):
    id: str
    community_id: str
    title: str
    media_url: str
    media: Optional[MediaOut] = None  # NEW
