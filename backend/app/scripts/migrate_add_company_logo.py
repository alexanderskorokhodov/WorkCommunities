"""
One-off lightweight migration: add companies.logo_media_id if missing.

Usage (Docker):
  docker compose exec api python -m app.scripts.migrate_add_company_logo

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
    return any(r[1] == column for r in rows)  # (cid, name, type, ...)


async def main():
    db_url = str(settings.DATABASE_URL)
    is_pg = db_url.startswith("postgresql")

    async with engine.begin() as conn:
        if is_pg:
            has_col = await _pg_has_column(conn, "companies", "logo_media_id")
            if not has_col:
                await conn.execute(text("ALTER TABLE companies ADD COLUMN logo_media_id VARCHAR NULL"))
                # optional index (safe, IF NOT EXISTS supported in Postgres)
                await conn.execute(text("CREATE INDEX IF NOT EXISTS ix_companies_logo_media_id ON companies (logo_media_id)"))
                print("Added column companies.logo_media_id (Postgres)")
            else:
                print("Column companies.logo_media_id already exists (Postgres)")
        else:
            has_col = await _sqlite_has_column(conn, "companies", "logo_media_id")
            if not has_col:
                await conn.execute(text("ALTER TABLE companies ADD COLUMN logo_media_id TEXT NULL"))
                print("Added column companies.logo_media_id (SQLite)")
            else:
                print("Column companies.logo_media_id already exists (SQLite)")


if __name__ == "__main__":
    asyncio.run(main())

