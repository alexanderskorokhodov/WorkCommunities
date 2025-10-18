"""
Drop columns posts.author_user_id and posts.featured.

Usage (Docker):
  docker compose exec api python -m app.scripts.migrate_drop_post_author_and_featured

Idempotent and safe across Postgres and SQLite. For SQLite, the table is
recreated due to limited ALTER TABLE support.
"""

import asyncio
from sqlalchemy import text

from app.adapters.db import engine
from app.core.config import settings


async def _pg_has_column(conn, table: str, column: str) -> bool:
    q = text(
        """
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = :table AND column_name = :column
        LIMIT 1
        """
    )
    res = await conn.execute(q, {"table": table, "column": column})
    return res.scalar_one_or_none() is not None


async def _sqlite_has_column(conn, table: str, column: str) -> bool:
    q = text(f"PRAGMA table_info({table})")
    res = await conn.execute(q)
    rows = res.fetchall()
    return any(r[1] == column for r in rows)


async def main():
    db_url = str(settings.DATABASE_URL)
    is_pg = db_url.startswith("postgresql")

    async with engine.begin() as conn:
        if is_pg:
            if await _pg_has_column(conn, "posts", "author_user_id"):
                await conn.execute(text("ALTER TABLE posts DROP COLUMN IF EXISTS author_user_id"))
                print("Dropped posts.author_user_id (Postgres)")
            else:
                print("Column posts.author_user_id already absent (Postgres)")

            if await _pg_has_column(conn, "posts", "featured"):
                await conn.execute(text("ALTER TABLE posts DROP COLUMN IF EXISTS featured"))
                print("Dropped posts.featured (Postgres)")
            else:
                print("Column posts.featured already absent (Postgres)")
        else:
            # SQLite: recreate table if any of the columns are present
            has_author = await _sqlite_has_column(conn, "posts", "author_user_id")
            has_featured = await _sqlite_has_column(conn, "posts", "featured")
            if not (has_author or has_featured):
                print("Columns already absent (SQLite)")
                return

            # Ensure foreign keys off during table rebuild
            await conn.execute(text("PRAGMA foreign_keys=OFF"))

            # Create new table without the dropped columns
            await conn.execute(text(
                """
                CREATE TABLE IF NOT EXISTS posts_new (
                    id TEXT PRIMARY KEY,
                    community_id TEXT,
                    title TEXT,
                    body TEXT,
                    created_at DATETIME
                )
                """
            ))

            # Copy data across
            await conn.execute(text(
                "INSERT INTO posts_new (id, community_id, title, body, created_at)\n"
                "SELECT id, community_id, title, body, created_at FROM posts"
            ))

            # Replace old table
            await conn.execute(text("DROP TABLE posts"))
            await conn.execute(text("ALTER TABLE posts_new RENAME TO posts"))

            # Restore indexes
            await conn.execute(text("CREATE INDEX IF NOT EXISTS ix_posts_community_id ON posts (community_id)"))

            # Re-enable foreign keys
            await conn.execute(text("PRAGMA foreign_keys=ON"))
            print("Recreated posts table without dropped columns (SQLite)")


if __name__ == "__main__":
    asyncio.run(main())

