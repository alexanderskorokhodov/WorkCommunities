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


async def main():
    async with engine.begin() as conn:
        dialect = conn.dialect.name
        if dialect.startswith("postgres"):
            await conn.execute(text(CREATE_TABLE_SQL_PG))
            await conn.execute(text(CREATE_INDEX_SQL_PG))
            print("Ensured cases table exists (Postgres)")
        else:
            await conn.execute(text(CREATE_TABLE_SQL_SQLITE))
            await conn.execute(text(CREATE_INDEX_SQL_SQLITE))
            print("Ensured cases table exists (SQLite)")


if __name__ == "__main__":
    asyncio.run(main())
