"""
Attach a given media to posts.

Default media id: bcc16aa8559048c18f67b69ef41083f9

Usage (Docker):
  # Only posts without any media (default)
  docker compose exec api python -m app.scripts.add_media_to_posts_without \
    --media-id bcc16aa8559048c18f67b69ef41083f9

  # Force attach to ALL posts that don't already have this media id
  docker compose exec api python -m app.scripts.add_media_to_posts_without \
    --media-id <uid> --force
  # Also supports values: --force 1 | true | yes

Notes:
- Idempotent: never creates duplicate post_media entries due to selection.
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


def _str2bool(v) -> bool:
    if isinstance(v, bool):
        return v
    if v is None:
        return True
    return str(v).strip().lower() in ("1", "true", "yes", "y", "on")


async def attach_media_to_all_missing_specific(media_id: str) -> int:
    """Attach media to all posts that do NOT already have this specific media id.
    Posts that already have it are skipped. Returns count of posts updated.
    """
    updated = 0
    async with async_session() as session:
        res = await session.execute(
            select(PostModel.id)
            .outerjoin(
                PostMediaModel,
                (PostMediaModel.post_id == PostModel.id) & (PostMediaModel.media_id == media_id),
            )
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
    parser = argparse.ArgumentParser(description="Attach media to posts")
    parser.add_argument("media_id_pos", nargs="?", help="Optional positional media id")
    parser.add_argument("--media-id", dest="media_id", default=DEFAULT_MEDIA_ID, help="Media id to attach (overridden by positional)")
    parser.add_argument(
        "--force",
        nargs="?",
        const=True,
        default=False,
        type=_str2bool,
        help="Attach to all posts (not only empty), skipping only those that already have this media id.",
    )
    args = parser.parse_args(argv)

    effective_media_id = args.media_id_pos or args.media_id

    await ensure_tables()
    await ensure_media(effective_media_id)
    if args.force:
        count = await attach_media_to_all_missing_specific(effective_media_id)
    else:
        count = await attach_media_to_posts_without(effective_media_id)
    print(f"Updated posts: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
