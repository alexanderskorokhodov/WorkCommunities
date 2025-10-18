"""
Bulk-set logo_media_id for all companies and communities.

By default sets only where the field is NULL. Use --force to overwrite existing values.

Usage (Docker):
  docker compose exec api python -m app.scripts.set_default_logos \
    --logo-id e0bee682aa83422db1463cfbcb4acd73

Options:
  --logo-id <uid>   Media id to set (default: e0bee682aa83422db1463cfbcb4acd73)
  --force           Overwrite existing non-null values

The script is idempotent and can add missing columns if absent.
"""

from __future__ import annotations

import argparse
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


async def _ensure_columns(conn, is_pg: bool) -> None:
    # companies.logo_media_id
    if is_pg:
        if not await _pg_has_column(conn, "companies", "logo_media_id"):
            await conn.execute(text("ALTER TABLE companies ADD COLUMN logo_media_id VARCHAR NULL"))
            await conn.execute(text("CREATE INDEX IF NOT EXISTS ix_companies_logo_media_id ON companies (logo_media_id)"))
        if not await _pg_has_column(conn, "communities", "logo_media_id"):
            await conn.execute(text("ALTER TABLE communities ADD COLUMN logo_media_id VARCHAR NULL"))
            await conn.execute(text("CREATE INDEX IF NOT EXISTS ix_communities_logo_media_id ON communities (logo_media_id)"))
    else:
        if not await _sqlite_has_column(conn, "companies", "logo_media_id"):
            await conn.execute(text("ALTER TABLE companies ADD COLUMN logo_media_id TEXT NULL"))
        if not await _sqlite_has_column(conn, "communities", "logo_media_id"):
            await conn.execute(text("ALTER TABLE communities ADD COLUMN logo_media_id TEXT NULL"))


async def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Set default logos for companies and communities")
    parser.add_argument("--logo-id", default="e0bee682aa83422db1463cfbcb4acd73", help="Media id to set")
    parser.add_argument("--force", action="store_true", help="Overwrite existing values")
    args = parser.parse_args(argv)

    db_url = str(settings.DATABASE_URL)
    is_pg = db_url.startswith("postgresql")

    async with engine.begin() as conn:
        await _ensure_columns(conn, is_pg=is_pg)

        condition = "" if args.force else " WHERE logo_media_id IS NULL"

        res1 = await conn.execute(text(f"UPDATE companies SET logo_media_id = :mid{condition}"), {"mid": args.logo_id})
        res2 = await conn.execute(text(f"UPDATE communities SET logo_media_id = :mid{condition}"), {"mid": args.logo_id})

        c1 = getattr(res1, "rowcount", -1)
        c2 = getattr(res2, "rowcount", -1)
        print(f"Updated companies: {c1}")
        print(f"Updated communities: {c2}")

    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))

