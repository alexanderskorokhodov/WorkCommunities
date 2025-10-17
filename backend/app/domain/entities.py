from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    id: str
    role: str  # "student" | "company"
    phone: Optional[str]
    email: Optional[str]
    password_hash: Optional[str]
    created_at: datetime


@dataclass
class Profile:
    id: str
    user_id: str
    full_name: Optional[str]
    city: Optional[str]
    interests: list[str]


@dataclass
class Company:
    id: str
    name: str
    description: Optional[str]


@dataclass
class Community:
    id: str
    company_id: Optional[str]
    name: str
    tags: list[str]
    is_archived: bool


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
class Post:
    id: str
    community_id: str
    author_user_id: str
    title: str
    body: str
    featured: bool
    created_at: datetime


@dataclass
class Story:
    id: str
    community_id: str
    title: str
    media_url: str
    created_at: datetime


@dataclass
class Event:
    id: str
    community_id: str
    title: str
    starts_at: datetime
    city: str | None


@dataclass
class OTP:
    id: str
    phone: str
    code: str
    expires_at: datetime
    consumed: bool
