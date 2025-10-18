"""
Attach a given media to all posts that currently have no media.

Default media id: bcc16aa8559048c18f67b69ef41083f9

Usage (Docker):
  docker compose exec api python -m app.scripts.add_media_to_posts_without \
    --media-id bcc16aa8559048c18f67b69ef41083f9

Notes:
- Idempotent: only creates PostMedia rows for posts lacking media.
- Ensures the media exists; if not, creates a placeholder Media entry.
"""

from __future__ import annotations

import argparse
import asyncio
from datetime import datetime

from sqlalchemy import select

from app.adapters.db import async_session, engine
from app.infrastructure.repos.sql_models import (
    Base,
    PostModel,
    PostMediaModel,
    MediaModel,
)


DEFAULT_MEDIA_ID = "bcc16aa8559048c18f67b69ef41083f9"


async def ensure_tables() -> None:
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


async def attach_media_to_posts_without(media_id: str) -> int:
    """Attach media to all posts that have no media yet. Returns count of posts updated."""
    updated = 0
    async with async_session() as session:
        # Find posts with no related post_media rows using OUTER JOIN
        res = await session.execute(
            select(PostModel.id)
            .outerjoin(PostMediaModel, PostMediaModel.post_id == PostModel.id)
            .where(PostMediaModel.id.is_(None))
        )
        post_ids = [row[0] for row in res.all()]

        for pid in post_ids:
            pm = PostMediaModel(post_id=pid, media_id=media_id, order_index=0)
            session.add(pm)
            updated += 1

        if updated:
            await session.commit()

    return updated


async def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Attach media to posts without media")
    parser.add_argument("--media-id", default=DEFAULT_MEDIA_ID, help="Media id to attach")
    args = parser.parse_args(argv)

    await ensure_tables()
    await ensure_media(args.media_id)
    count = await attach_media_to_posts_without(args.media_id)
    print(f"Updated posts: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
