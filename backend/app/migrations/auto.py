import asyncio
from sqlalchemy import text

from app.adapters.db import engine


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


async def run_lightweight_migrations():
    async with engine.begin() as conn:
        dialect = conn.dialect.name
        is_pg = dialect.startswith("postgres")

        # communities.description
        if is_pg:
            if not await _pg_has_column(conn, "communities", "description"):
                await conn.execute(text("ALTER TABLE communities ADD COLUMN description TEXT NULL"))
            if not await _pg_has_column(conn, "communities", "telegram_url"):
                await conn.execute(text("ALTER TABLE communities ADD COLUMN telegram_url VARCHAR NULL"))
            if not await _pg_has_column(conn, "communities", "tags"):
                await conn.execute(text("ALTER TABLE communities ADD COLUMN tags TEXT NULL"))
            if not await _pg_has_column(conn, "communities", "is_archived"):
                await conn.execute(text("ALTER TABLE communities ADD COLUMN is_archived BOOLEAN NOT NULL DEFAULT FALSE"))
        else:
            if not await _sqlite_has_column(conn, "communities", "description"):
                await conn.execute(text("ALTER TABLE communities ADD COLUMN description TEXT NULL"))
            if not await _sqlite_has_column(conn, "communities", "telegram_url"):
                await conn.execute(text("ALTER TABLE communities ADD COLUMN telegram_url TEXT NULL"))
            if not await _sqlite_has_column(conn, "communities", "tags"):
                await conn.execute(text("ALTER TABLE communities ADD COLUMN tags TEXT NULL"))
            if not await _sqlite_has_column(conn, "communities", "is_archived"):
                await conn.execute(text("ALTER TABLE communities ADD COLUMN is_archived BOOLEAN NOT NULL DEFAULT 0"))

        # companies.logo_media_id + tags
        if is_pg:
            if not await _pg_has_column(conn, "companies", "logo_media_id"):
                await conn.execute(text("ALTER TABLE companies ADD COLUMN logo_media_id VARCHAR NULL"))
            if not await _pg_has_column(conn, "companies", "tags"):
                await conn.execute(text("ALTER TABLE companies ADD COLUMN tags TEXT NULL"))
        else:
            if not await _sqlite_has_column(conn, "companies", "logo_media_id"):
                await conn.execute(text("ALTER TABLE companies ADD COLUMN logo_media_id TEXT NULL"))
            if not await _sqlite_has_column(conn, "companies", "tags"):
                await conn.execute(text("ALTER TABLE companies ADD COLUMN tags TEXT NULL"))

        # users.avatar_media_id
        if is_pg:
            if not await _pg_has_column(conn, "users", "avatar_media_id"):
                await conn.execute(text("ALTER TABLE users ADD COLUMN avatar_media_id VARCHAR NULL"))
        else:
            if not await _sqlite_has_column(conn, "users", "avatar_media_id"):
                await conn.execute(text("ALTER TABLE users ADD COLUMN avatar_media_id TEXT NULL"))


def main():
    asyncio.run(run_lightweight_migrations())


if __name__ == "__main__":
    main()

