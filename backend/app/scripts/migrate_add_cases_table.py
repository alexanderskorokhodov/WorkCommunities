"""
Lightweight migration: create cases table if it doesn't exist.

Fields:
- id (uid, PK)
- community_id (FK -> communities.id)
- title (str)
- description (text, nullable)
- date (timestamp)
- solutions_count (int, default 0)

Usage (Docker):
  docker compose exec api python -m app.scripts.migrate_add_cases_table

Idempotent: safe to run multiple times.
"""

import asyncio
from sqlalchemy import text

from app.adapters.db import engine


CREATE_TABLE_SQL_PG = """
CREATE TABLE IF NOT EXISTS cases (
    id VARCHAR PRIMARY KEY,
    community_id VARCHAR NOT NULL REFERENCES communities(id),
    title VARCHAR NOT NULL,
    description TEXT NULL,
    date TIMESTAMP NOT NULL,
    solutions_count INTEGER NOT NULL DEFAULT 0
)
"""

CREATE_INDEX_SQL_PG = """
CREATE INDEX IF NOT EXISTS ix_cases_community_id ON cases (community_id)
"""

CREATE_TABLE_SQL_SQLITE = """
CREATE TABLE IF NOT EXISTS cases (
    id TEXT PRIMARY KEY,
    community_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NULL,
    date TEXT NOT NULL,
    solutions_count INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY(community_id) REFERENCES communities(id)
)
"""

CREATE_INDEX_SQL_SQLITE = """
CREATE INDEX IF NOT EXISTS ix_cases_community_id ON cases (community_id)
"""


async def _ensure_table_and_index(conn) -> str:
    dialect = conn.dialect.name
    if dialect.startswith("postgres"):
        await conn.execute(text(CREATE_TABLE_SQL_PG))
        await conn.execute(text(CREATE_INDEX_SQL_PG))
        print("Ensured cases table exists (Postgres)")
        return "postgres"
    else:
        await conn.execute(text(CREATE_TABLE_SQL_SQLITE))
        await conn.execute(text(CREATE_INDEX_SQL_SQLITE))
        print("Ensured cases table exists (SQLite)")
        return "sqlite"


async def _migrate_points_to_solutions_count(conn, flavor: str) -> None:
    """Rename cases.points -> cases.solutions_count (or add/copy if needed)."""
    try:
        if flavor == "postgres":
            cols = (await conn.execute(text("""
                SELECT column_name FROM information_schema.columns
                WHERE table_name='cases'
            """))).scalars().all()
            cols = set(cols)
            if "solutions_count" not in cols and "points" in cols:
                await conn.execute(text("ALTER TABLE cases RENAME COLUMN points TO solutions_count"))
                print("Renamed cases.points -> solutions_count (Postgres)")
            elif "solutions_count" not in cols and "points" not in cols:
                await conn.execute(text("ALTER TABLE cases ADD COLUMN solutions_count INTEGER NOT NULL DEFAULT 0"))
                print("Added cases.solutions_count (Postgres)")
        else:  # sqlite
            # Inspect columns
            res = await conn.execute(text("PRAGMA table_info('cases')"))
            cols = {row[1] for row in res.fetchall()}  # row[1] is name
            if "solutions_count" not in cols and "points" in cols:
                try:
                    await conn.execute(text("ALTER TABLE cases RENAME COLUMN points TO solutions_count"))
                    print("Renamed cases.points -> solutions_count (SQLite)")
                except Exception:
                    # Fallback: add column if possible, then copy values
                    await conn.execute(text("ALTER TABLE cases ADD COLUMN solutions_count INTEGER NOT NULL DEFAULT 0"))
                    try:
                        await conn.execute(text("UPDATE cases SET solutions_count = points"))
                    except Exception:
                        pass
                    print("Added and populated cases.solutions_count (SQLite fallback)")
            elif "solutions_count" not in cols and "points" not in cols:
                await conn.execute(text("ALTER TABLE cases ADD COLUMN solutions_count INTEGER NOT NULL DEFAULT 0"))
                print("Added cases.solutions_count (SQLite)")
    except Exception as e:
        print(f"Warning: migration for cases.solutions_count skipped: {e}")


async def main():
    async with engine.begin() as conn:
        flavor = await _ensure_table_and_index(conn)
        await _migrate_points_to_solutions_count(conn, flavor)


if __name__ == "__main__":
    asyncio.run(main())
