"""
Create a default post for each community if it has no posts yet.

Title: "Онлайн-воркшоп от R-Farm с Василием Игнатьевым"
Body:
  Уже в эту пятницу приглашаем на встречу с Василием Игнатьевым, экспертом R-Farm по биотехнологическим инновациям.

  Разберём реальные кейсы из индустрии, поговорим о карьере в фарме и разложим по полочкам, как молодым специалистам попасть в проекты R-Farm.

Attach media id: c24cf1a93624475a8e19b7f1f0d30f27

Usage (Docker):
  docker compose exec api python -m app.scripts.seed_workshop_posts_for_communities

Idempotent: only creates posts for communities without any posts.
"""

import asyncio
from datetime import datetime

from sqlalchemy import select

from app.adapters.db import async_session, engine
from app.infrastructure.repos.sql_models import Base, CommunityModel, ContentModel, ContentMediaModel, MediaModel


WORKSHOP_TITLE = "Онлайн-воркшоп от R-Farm с Василием Игнатьевым"
WORKSHOP_BODY = (
    "Уже в эту пятницу приглашаем на встречу с Василием Игнатьевым, экспертом R-Farm по биотехнологическим инновациям.\n\n"
    "Разберём реальные кейсы из индустрии, поговорим о карьере в фарме и разложим по полочкам, как молодым специалистам попасть в проекты R-Farm."
)
MEDIA_ID = "c24cf1a93624475a8e19b7f1f0d30f27"


async def ensure_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def ensure_media(media_id: str) -> MediaModel:
    async with async_session() as session:
        res = await session.execute(select(MediaModel).where(MediaModel.id == media_id))
        existing = res.scalar_one_or_none()
        if existing:
            return existing
        m = MediaModel(
            id=media_id,
            kind="image",
            mime="image/jpeg",
            ext="jpg",
            size=0,
            url=f"/media/{media_id}",
            created_at=datetime.utcnow(),
        )
        session.add(m)
        await session.commit()
        await session.refresh(m)
        return m


async def seed_workshop_posts():
    created = 0
    media = await ensure_media(MEDIA_ID)
    async with async_session() as session:
        res = await session.execute(select(CommunityModel))
        communities = res.scalars().all()
        for c in communities:
            res_posts = await session.execute(
                select(ContentModel).where(ContentModel.community_id == c.id, ContentModel.type == "post")
            )
            has_post = res_posts.first() is not None
            if has_post:
                continue

            p = ContentModel(
                community_id=c.id,
                type="post",
                title=WORKSHOP_TITLE,
                body=WORKSHOP_BODY,
                created_at=datetime.utcnow(),
            )
            session.add(p)
            await session.flush()

            pm = ContentMediaModel(content_id=p.id, media_id=media.id, order_index=0)
            session.add(pm)

            created += 1

        await session.commit()
    print(f"Created {created} workshop post(s) for communities without posts.")


async def main():
    await ensure_tables()
    await seed_workshop_posts()


if __name__ == "__main__":
    asyncio.run(main())
