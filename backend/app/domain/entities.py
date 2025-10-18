from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


@dataclass
class User:
    id: str
    role: str  # "student" | "company" | "admin"
    phone: Optional[str]
    email: Optional[str]
    password_hash: Optional[str]
    created_at: datetime
    avatar_media_id: Optional[str] = None


@dataclass
class Profile:
    id: str
    user_id: str
    full_name: Optional[str]
    portfolio_url: Optional[str]
    description: Optional[str]
    skills: list["Skill"]
    statuses: list["Status"]


@dataclass
class Sphere:
    id: str  # uid
    title: str
    background_color: str
    text_color: str


@dataclass
class Skill:
    id: str  # uid
    title: str
    sphere_id: str
    sphere: Optional[Sphere] = None


@dataclass
class Status:
    id: str  # uid
    title: str


@dataclass
class Company:
    id: str
    name: str
    description: Optional[str]
    logo_media_id: Optional[str] = None
    tags: list[str] = field(default_factory=list)


@dataclass
class Community:
    id: str
    company_id: Optional[str]
    name: str
    description: Optional[str]
    telegram_url: Optional[str]
    tags: list[str]
    is_archived: bool
    logo_media_id: Optional[str] = None


@dataclass
class Membership:
    id: str
    user_id: str
    community_id: str
    role: str  # member | admin


@dataclass
class Follow:
    id: str
    user_id: str
    community_id: str

@dataclass
class CompanyFollow:
    id: str
    user_id: str
    company_id: str


@dataclass
class Post:
    id: str
    community_id: str
    title: str
    body: str
    created_at: datetime
    # unified content extensions
    tags: list[str] = field(default_factory=list)
    skills: list["Skill"] = field(default_factory=list)
    cost: Optional[int] = None
    participant_payout: Optional[int] = None


@dataclass
class Story:
    id: str
    company_id: str
    title: str
    media_url: str
    created_at: datetime


@dataclass
class Event:
    id: str
    community_id: str
    title: str
    event_date: datetime
    city: str | None
    location: str | None = None
    description: str | None = None
    registration: str | None = None
    format: str | None = None
    media_id: str | None = None
    # unified content extensions
    tags: list[str] = field(default_factory=list)
    skills: list["Skill"] = field(default_factory=list)
    cost: Optional[int] = None
    participant_payout: Optional[int] = None


@dataclass
class EventParticipant:
    id: str
    user_id: str
    event_id: str


@dataclass
class OTP:
    id: str
    phone: str
    code: str
    expires_at: datetime
    consumed: bool


class MediaType(str, Enum):
    image = "image"
    video = "video"
    other = "other"


@dataclass
class Media:
    id: str  # uid
    kind: MediaType
    mime: str
    ext: str | None
    size: int
    url: str  # публичная ссылка /media/{id}
    created_at: datetime


@dataclass
class Case:
    id: str
    community_id: str
    title: str
    description: Optional[str]
    date: datetime
    points: int
