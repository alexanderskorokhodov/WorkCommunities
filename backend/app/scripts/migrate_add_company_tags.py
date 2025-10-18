"""
One-off lightweight migration: add companies.tags if missing.

Usage (Docker):
  docker compose exec api python -m app.scripts.migrate_add_company_tags

Idempotent: safe to run multiple times.
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
            if not await _pg_has_column(conn, "companies", "tags"):
                await conn.execute(text("ALTER TABLE companies ADD COLUMN tags VARCHAR NULL"))
                print("Added column companies.tags (Postgres)")
            else:
                print("Column companies.tags already exists (Postgres)")
        else:
            if not await _sqlite_has_column(conn, "companies", "tags"):
                await conn.execute(text("ALTER TABLE companies ADD COLUMN tags TEXT NULL"))
                print("Added column companies.tags (SQLite)")
            else:
                print("Column companies.tags already exists (SQLite)")


if __name__ == "__main__":
    asyncio.run(main())

