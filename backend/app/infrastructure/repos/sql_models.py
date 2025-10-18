import uuid
from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, ForeignKey, Text, Integer, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


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
    portfolio_url: Mapped[str | None] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(Text)


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
    description: Mapped[str | None] = mapped_column(Text)
    telegram_url: Mapped[str | None] = mapped_column(String)
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

class CompanyFollowModel(Base):
    __tablename__ = "company_follows"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uid)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    company_id: Mapped[str] = mapped_column(ForeignKey("companies.id"), index=True)


class PostModel(Base):
    __tablename__ = "posts"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uid)
    community_id: Mapped[str] = mapped_column(ForeignKey("communities.id"), index=True)
    author_user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String)
    body: Mapped[str] = mapped_column(Text)
    featured: Mapped[bool] = mapped_column(Boolean, default=False)
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

    def __str__(self):
        return f'Id: {self.phone}, Code: {self.code}, Expires: {self.expires_at}, Consumed: {self.consumed}'


class MediaModel(Base):
    __tablename__ = "media"
    id: Mapped[str] = mapped_column(String, primary_key=True)  # uid генерим сами
    kind: Mapped[str] = mapped_column(String, index=True)  # image | video | other
    mime: Mapped[str] = mapped_column(String)
    ext: Mapped[str | None] = mapped_column(String, nullable=True)
    size: Mapped[int] = mapped_column(Integer)
    url: Mapped[str] = mapped_column(String)  # /media/{id}
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class PostMediaModel(Base):
    __tablename__ = "post_media"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uid)
    post_id: Mapped[str] = mapped_column(ForeignKey("posts.id"), index=True)
    media_id: Mapped[str] = mapped_column(ForeignKey("media.id"), index=True)
    order_index: Mapped[int] = mapped_column(Integer, default=0)
    __table_args__ = (UniqueConstraint("post_id", "media_id", name="uq_post_media"),)


class StoryModel(Base):
    __tablename__ = "stories"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uid)
    company_id: Mapped[str] = mapped_column(ForeignKey("companies.id"), index=True)
    title: Mapped[str] = mapped_column(String)
    media_url: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    media_id: Mapped[str | None] = mapped_column(ForeignKey("media.id"), index=True)  # NEW


# NEW — справочники сфер/навыков/статусов и связи профиля
class SphereModel(Base):
    __tablename__ = "spheres"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uid)  # uid
    title: Mapped[str] = mapped_column(String)
    background_color: Mapped[str] = mapped_column(String)  # hex
    text_color: Mapped[str] = mapped_column(String)  # hex


class SkillModel(Base):
    __tablename__ = "skills"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uid)  # uid
    title: Mapped[str] = mapped_column(String)
    sphere_id: Mapped[str] = mapped_column(ForeignKey("spheres.id"), index=True)


class StatusModel(Base):
    __tablename__ = "statuses"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uid)  # uid
    title: Mapped[str] = mapped_column(String)


class ProfileSkillModel(Base):
    __tablename__ = "profile_skills"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uid)
    profile_id: Mapped[str] = mapped_column(ForeignKey("profiles.id"), index=True)
    skill_id: Mapped[str] = mapped_column(ForeignKey("skills.id"), index=True)
    __table_args__ = (UniqueConstraint("profile_id", "skill_id", name="uq_profile_skill"),)


class ProfileStatusModel(Base):
    __tablename__ = "profile_statuses"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uid)
    profile_id: Mapped[str] = mapped_column(ForeignKey("profiles.id"), index=True)
    status_id: Mapped[str] = mapped_column(ForeignKey("statuses.id"), index=True)
    __table_args__ = (UniqueConstraint("profile_id", "status_id", name="uq_profile_status"),)
