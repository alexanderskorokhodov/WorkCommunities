import asyncio
import random
import string
from datetime import datetime

from sqlalchemy import select

from app.adapters.db import engine, async_session
from app.infrastructure.repos.sql_models import (
    Base,
    UserModel,
    CompanyModel,
    CommunityModel,
    ContentModel,
    StoryModel,
    MediaModel,
)


def _suffix(n: int) -> str:
    return f"{n:02d}"


async def ensure_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def create_student_user(idx: int) -> UserModel:
    async with async_session() as session:
        phone = f"+7999000{idx:04d}"
        res = await session.execute(select(UserModel).where(UserModel.phone == phone))
        existing = res.scalar_one_or_none()
        if existing:
            return existing
        u = UserModel(role="student", phone=phone, email=None, password_hash=None)
        session.add(u)
        await session.commit()
        await session.refresh(u)
        return u


async def create_company(idx: int) -> CompanyModel:
    async with async_session() as session:
        name = f"Mock Company {_suffix(idx)}"
        res = await session.execute(select(CompanyModel).where(CompanyModel.name == name))
        existing = res.scalar_one_or_none()
        if existing:
            return existing
        c = CompanyModel(name=name, description=f"Описание компании {name}")
        session.add(c)
        await session.commit()
        await session.refresh(c)
        return c


async def create_community(company_id: str, idx: int) -> CommunityModel:
    async with async_session() as session:
        name = f"Community {_suffix(idx)}"
        res = await session.execute(
            select(CommunityModel).where(CommunityModel.company_id == company_id, CommunityModel.name == name)
        )
        existing = res.scalar_one_or_none()
        if existing:
            return existing
        c = CommunityModel(
            company_id=company_id,
            name=name,
            description=f"Описание для {name}",
            tags=",".join(["mock", "test", _suffix(idx)]),
            telegram_url=None,
            is_archived=False,
        )
        session.add(c)
        await session.commit()
        await session.refresh(c)
        return c


async def create_post(community_id: str, idx: int) -> ContentModel:
    async with async_session() as session:
        title = f"Пост {_suffix(idx)}"
        body = "\n".join([
            "Это тестовый пост для проверки интерфейса.",
            "В нём могут быть переносы строк и разная длина описаний.",
        ])
        p = ContentModel(
            community_id=community_id,
            type="post",
            title=title,
            body=body,
            created_at=datetime.utcnow(),
        )
        session.add(p)
        await session.commit()
        await session.refresh(p)
        return p


async def create_media(image_idx: int) -> MediaModel:
    async with async_session() as session:
        # deterministic id by not exposing; DB will set uid default elsewhere in app, here we rely on COMMIT refresh
        url = f"/media/mock_{_suffix(image_idx)}.jpg"
        m = MediaModel(
            id=f"mock{_suffix(image_idx)}{_suffix(image_idx)}{_suffix(image_idx)}",  # stable uid-like
            kind="image",
            mime="image/jpeg",
            ext="jpg",
            size=123456,
            url=url,
            created_at=datetime.utcnow(),
        )
        session.add(m)
        await session.commit()
        await session.refresh(m)
        return m


async def create_story(company_id: str, idx: int) -> StoryModel:
    media = await create_media(idx)
    async with async_session() as session:
        s = StoryModel(
            company_id=company_id,
            title=f"Сторис {_suffix(idx)}",
            media_url=media.url,
            created_at=datetime.utcnow(),
            media_id=media.id,
        )
        session.add(s)
        await session.commit()
        await session.refresh(s)
        return s


async def create_event(community_id: str, idx: int) -> ContentModel:
    async with async_session() as session:
        e = ContentModel(
            community_id=community_id,
            type="event",
            title=f"Ивент {_suffix(idx)}",
            event_date=datetime.utcnow(),
            city="Москва",
            location="Онлайн",
            description="Тестовый ивент с переносами\nи подробным описанием.",
            registration="https://example.com/register",
            format="online",
            media_id=None,
            created_at=datetime.utcnow(),
        )
        session.add(e)
        await session.commit()
        await session.refresh(e)
        return e


async def generate():
    await ensure_tables()

    # Users
    users = [await create_student_user(i) for i in range(1, 6)]

    # Companies and communities
    companies = [await create_company(i) for i in range(1, 4)]
    communities: list[CommunityModel] = []
    for i, comp in enumerate(companies, start=1):
        for j in range(1, 3):  # 2 communities per company
            communities.append(await create_community(comp.id, i * 10 + j))

    # Posts
    for k, comm in enumerate(communities, start=1):
        # 3 posts per community
        for pidx in range(1, 4):
            await create_post(comm.id, k * 10 + pidx)

    # Stories per company (2 each) and events per community (2 each)
    for i, comp in enumerate(companies, start=1):
        await create_story(comp.id, i * 10 + 1)
        await create_story(comp.id, i * 10 + 2)
    for j, comm in enumerate(communities, start=1):
        await create_event(comm.id, j * 10 + 1)
        await create_event(comm.id, j * 10 + 2)

    print("Mock data generated: users, companies, communities, posts, stories, events.")


def main():
    asyncio.run(generate())


if __name__ == "__main__":
    main()
