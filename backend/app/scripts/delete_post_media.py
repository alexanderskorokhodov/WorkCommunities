"""
Delete all media attachments from posts.

What it does:
- Deletes all rows from `post_media` (unlinking media from posts).
- Optional: delete orphaned `media` rows not referenced anywhere else (`--delete-orphaned`).
- Optional: dry run to see counts without modifying data (`--dry-run`).

Usage (Docker):
  # Remove all post-media links
  docker compose exec api python -m app.scripts.delete_post_media

  # Dry run (show counts only)
  docker compose exec api python -m app.scripts.delete_post_media --dry-run

  # Also delete orphaned media rows (not used by posts, users, companies, communities, events, stories)
  docker compose exec api python -m app.scripts.delete_post_media --delete-orphaned

Notes:
- Idempotent: running again after deletion makes no changes.
- Orphan cleanup affects DB rows only; it does not remove files from storage.
"""

from __future__ import annotations

import argparse
import asyncio

from sqlalchemy import select, func, delete, exists

from app.adapters.db import async_session, engine
from app.infrastructure.repos.sql_models import (
    Base,
    PostMediaModel,
    MediaModel,
    UserModel,
    CompanyModel,
    CommunityModel,
    EventModel,
    StoryModel,
)


async def ensure_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def count_post_media() -> int:
    async with async_session() as session:
        res = await session.execute(select(func.count()).select_from(PostMediaModel))
        return int(res.scalar() or 0)


async def delete_all_post_media() -> int:
    """Delete all rows from post_media. Returns deleted count."""
    async with async_session() as session:
        # Count first
        res = await session.execute(select(func.count()).select_from(PostMediaModel))
        total = int(res.scalar() or 0)
        if total:
            await session.execute(delete(PostMediaModel))
            await session.commit()
        return total


async def count_orphaned_media() -> int:
    async with async_session() as session:
        stmt = (
            select(func.count())
            .select_from(MediaModel)
            .where(~exists(select(1).where(PostMediaModel.media_id == MediaModel.id)))
            .where(~exists(select(1).where(UserModel.avatar_media_id == MediaModel.id)))
            .where(~exists(select(1).where(CompanyModel.logo_media_id == MediaModel.id)))
            .where(~exists(select(1).where(CommunityModel.logo_media_id == MediaModel.id)))
            .where(~exists(select(1).where(EventModel.media_id == MediaModel.id)))
            .where(~exists(select(1).where(StoryModel.media_id == MediaModel.id)))
        )
        res = await session.execute(stmt)
        return int(res.scalar() or 0)


async def delete_orphaned_media() -> int:
    """Delete media rows not referenced by any entity. Returns deleted count."""
    async with async_session() as session:
        # Count orphans first
        cnt = await count_orphaned_media()
        if cnt:
            stmt = (
                delete(MediaModel)
                .where(~exists(select(1).where(PostMediaModel.media_id == MediaModel.id)))
                .where(~exists(select(1).where(UserModel.avatar_media_id == MediaModel.id)))
                .where(~exists(select(1).where(CompanyModel.logo_media_id == MediaModel.id)))
                .where(~exists(select(1).where(CommunityModel.logo_media_id == MediaModel.id)))
                .where(~exists(select(1).where(EventModel.media_id == MediaModel.id)))
                .where(~exists(select(1).where(StoryModel.media_id == MediaModel.id)))
            )
            await session.execute(stmt)
            await session.commit()
        return cnt


def _str2bool(v) -> bool:
    if isinstance(v, bool):
        return v
    if v is None:
        return True
    return str(v).strip().lower() in ("1", "true", "yes", "y", "on")


async def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Delete all media attachments from posts")
    parser.add_argument("--dry-run", nargs="?", const=True, default=False, type=_str2bool,
                        help="Only show what would be deleted")
    parser.add_argument("--delete-orphaned", nargs="?", const=True, default=False, type=_str2bool,
                        help="Also delete orphaned media rows not referenced elsewhere")
    args = parser.parse_args(argv)

    await ensure_tables()

    links_before = await count_post_media()
    orphans_before = await count_orphaned_media()

    if args.dry_run:
        print(f"Would delete post-media links: {links_before}")
        if args.delete_orphaned:
            print(f"Would delete orphaned media rows: {orphans_before}")
        return 0

    deleted_links = await delete_all_post_media()
    print(f"Deleted post-media links: {deleted_links}")

    if args.delete_orphaned:
        deleted_media = await delete_orphaned_media()
        print(f"Deleted orphaned media rows: {deleted_media}")

    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))

