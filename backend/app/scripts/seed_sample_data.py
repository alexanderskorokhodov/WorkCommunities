import asyncio
import uuid
from datetime import datetime, timedelta

from sqlalchemy import select

from app.adapters.db import engine, async_session
from app.infrastructure.repos.sql_models import (
    Base,
    UserModel,
    CompanyModel,
    CommunityModel,
    PostModel,
    StoryModel,
    MediaModel,
    PostMediaModel,
)


def _uid() -> str:
    return uuid.uuid4().hex


async def ensure_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_or_create_company(name: str, description: str | None = None):
    async with async_session() as session:
        res = await session.execute(select(CompanyModel).where(CompanyModel.name == name))
        existing = res.scalar_one_or_none()
        if existing:
            return existing
        c = CompanyModel(name=name, description=description)
        session.add(c)
        await session.commit()
        await session.refresh(c)
        return c


async def get_or_create_user(role: str, phone: str | None, email: str | None):
    async with async_session() as session:
        q = select(UserModel)
        if phone:
            q = q.where(UserModel.phone == phone)
        elif email:
            q = q.where(UserModel.email == email)
        res = await session.execute(q)
        existing = res.scalar_one_or_none()
        if existing:
            return existing
        u = UserModel(role=role, phone=phone, email=email, password_hash=None)
        session.add(u)
        await session.commit()
        await session.refresh(u)
        return u


async def create_community(company_id: str, name: str, description: str | None = None, tags: str | None = None,
                           telegram_url: str | None = None):
    async with async_session() as session:
        # idempotency by (company_id, name)
        res = await session.execute(
            select(CommunityModel).where(CommunityModel.company_id == company_id, CommunityModel.name == name)
        )
        existing = res.scalar_one_or_none()
        if existing:
            return existing
        c = CommunityModel(company_id=company_id, name=name, description=description, tags=tags,
                           telegram_url=telegram_url, is_archived=False)
        session.add(c)
        await session.commit()
        await session.refresh(c)
        return c


async def create_post(community_id: str, author_user_id: str, title: str, body: str, featured: bool = False,
                      media_urls: list[str] | None = None):
    async with async_session() as session:
        p = PostModel(community_id=community_id, author_user_id=author_user_id, title=title, body=body,
                      featured=featured, created_at=datetime.utcnow())
        session.add(p)
        await session.flush()

        if media_urls:
            for i, url in enumerate(media_urls):
                mid = _uid()
                m = MediaModel(
                    id=mid,
                    kind="image",
                    mime="image/jpeg",
                    ext="jpg",
                    size=123456,
                    url=url or f"/media/{mid}",
                    created_at=datetime.utcnow(),
                )
                session.add(m)
                await session.flush()
                pm = PostMediaModel(post_id=p.id, media_id=m.id, order_index=i)
                session.add(pm)

        await session.commit()
        await session.refresh(p)
        return p


async def create_story(company_id: str, title: str, media_url: str):
    async with async_session() as session:
        # create media entry and link it to story via media_id
        mid = _uid()
        m = MediaModel(
            id=mid,
            kind="image",
            mime="image/jpeg",
            ext="jpg",
            size=234567,
            url=media_url or f"/media/{mid}",
            created_at=datetime.utcnow(),
        )
        session.add(m)
        await session.flush()

        s = StoryModel(company_id=company_id, title=title, media_url=m.url, media_id=m.id,
                        created_at=datetime.utcnow())
        session.add(s)
        await session.commit()
        await session.refresh(s)
        return s


async def seed():
    await ensure_tables()

    # Users to author posts
    user_main = await get_or_create_user(role="user", phone="+70000000001", email="user1@example.com")
    user_alt = await get_or_create_user(role="user", phone="+70000000002", email="user2@example.com")

    # Companies
    acme = await get_or_create_company("Acme Corp", "Инновационные решения для бизнеса")
    globex = await get_or_create_company("Globex", "Глобальные продукты и сервисы")

    # Communities
    acme_dev = await create_community(acme.id, "Acme Developers", "Сообщество разработчиков Acme", tags="dev,backend")
    acme_design = await create_community(acme.id, "Acme Design", "UI/UX и визуал", tags="design,uiux")
    globex_marketing = await create_community(globex.id, "Globex Marketing", "Маркетинг и рост", tags="marketing,growth")

    # Posts with optional media
    await create_post(
        community_id=acme_dev.id,
        author_user_id=user_main.id,
        title="Новый релиз платформы",
        body="Мы выпустили версию 2.0 с поддержкой async API.",
        featured=True,
        media_urls=[f"/media/{_uid()}"]
    )
    await create_post(
        community_id=acme_dev.id,
        author_user_id=user_alt.id,
        title="Гайд по миграции",
        body="Подробности миграции с 1.x на 2.0, чеклист и советы.",
        featured=False,
        media_urls=[]
    )
    await create_post(
        community_id=acme_design.id,
        author_user_id=user_main.id,
        title="Новые дизайн-токены",
        body="Добавили поддержку адаптивной типографики и цветовых тем.",
        featured=False,
        media_urls=[f"/media/{_uid()}", f"/media/{_uid()}"]
    )
    await create_post(
        community_id=globex_marketing.id,
        author_user_id=user_alt.id,
        title="Growth-инициативы Q4",
        body="Планируем кампании в соцсетях и партнерства с лидерами мнений.",
        featured=True
    )

    # Stories per company
    await create_story(acme.id, "День в офисе Acme", f"/media/{_uid()}")
    await create_story(acme.id, "Как мы готовим релизы", f"/media/{_uid()}")
    await create_story(globex.id, "За кулисами продукта", f"/media/{_uid()}")

    print("Seed completed: companies, communities, posts, stories created.")


def main():
    asyncio.run(seed())


if __name__ == "__main__":
    main()

