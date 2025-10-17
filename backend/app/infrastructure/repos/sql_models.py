
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Text
from datetime import datetime
import uuid

class Base(DeclarativeBase):
    pass

def uid() -> str:
    return uuid.uuid4().hex

class UserModel(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uid)
    role: Mapped[str] = mapped_column(String, index=True)
    phone: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    email: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    password_hash: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class ProfileModel(Base):
    __tablename__ = "profiles"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uid)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    full_name: Mapped[str | None] = mapped_column(String)
    city: Mapped[str | None] = mapped_column(String)
    interests: Mapped[str | None] = mapped_column(Text)  # comma-separated

class CompanyModel(Base):
    __tablename__ = "companies"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uid)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(Text)

class CommunityModel(Base):
    __tablename__ = "communities"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uid)
    company_id: Mapped[str | None] = mapped_column(ForeignKey("companies.id"))
    name: Mapped[str] = mapped_column(String, index=True)
    tags: Mapped[str | None] = mapped_column(Text)  # comma-separated
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)

class MembershipModel(Base):
    __tablename__ = "memberships"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uid)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    community_id: Mapped[str] = mapped_column(ForeignKey("communities.id"), index=True)
    role: Mapped[str] = mapped_column(String, default="member")

class FollowModel(Base):
    __tablename__ = "follows"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uid)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    community_id: Mapped[str] = mapped_column(ForeignKey("communities.id"), index=True)

class PostModel(Base):
    __tablename__ = "posts"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uid)
    community_id: Mapped[str] = mapped_column(ForeignKey("communities.id"), index=True)
    author_user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String)
    body: Mapped[str] = mapped_column(Text)
    featured: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class StoryModel(Base):
    __tablename__ = "stories"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uid)
    community_id: Mapped[str] = mapped_column(ForeignKey("communities.id"), index=True)
    title: Mapped[str] = mapped_column(String)
    media_url: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class EventModel(Base):
    __tablename__ = "events"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uid)
    community_id: Mapped[str] = mapped_column(ForeignKey("communities.id"), index=True)
    title: Mapped[str] = mapped_column(String)
    starts_at: Mapped[datetime] = mapped_column(DateTime)
    city: Mapped[str | None] = mapped_column(String)

class OTPModel(Base):
    __tablename__ = "otps"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uid)
    phone: Mapped[str] = mapped_column(String, index=True)
    code: Mapped[str] = mapped_column(String)
    expires_at: Mapped[datetime] = mapped_column(DateTime)
    consumed: Mapped[bool] = mapped_column(Boolean, default=False)
