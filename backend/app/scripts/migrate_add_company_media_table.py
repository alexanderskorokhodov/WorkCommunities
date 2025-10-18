"""
Create company_media table if it doesn't exist.

Fields:
- id (uid, PK)
- company_id (FK -> companies.id)
- media_id (FK -> media.id)
- order_index (int, default 0)

Usage (Docker):
  docker compose exec api python -m app.scripts.migrate_add_company_media_table

Idempotent: safe to run multiple times.
"""

import asyncio
from sqlalchemy import text

from app.adapters.db import engine


CREATE_TABLE_SQL_PG = """
CREATE TABLE IF NOT EXISTS company_media (
    id VARCHAR PRIMARY KEY,
    company_id VARCHAR NOT NULL REFERENCES companies(id),
    media_id VARCHAR NOT NULL REFERENCES media(id),
    order_index INTEGER NOT NULL DEFAULT 0,
    CONSTRAINT uq_company_media UNIQUE (company_id, media_id)
)
"""

CREATE_INDEXES_SQL_PG = [
    "CREATE INDEX IF NOT EXISTS ix_company_media_company ON company_media(company_id)",
    "CREATE INDEX IF NOT EXISTS ix_company_media_media ON company_media(media_id)",
]

CREATE_TABLE_SQL_SQLITE = """
CREATE TABLE IF NOT EXISTS company_media (
    id TEXT PRIMARY KEY,
    company_id TEXT NOT NULL,
    media_id TEXT NOT NULL,
    order_index INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY(company_id) REFERENCES companies(id),
    FOREIGN KEY(media_id) REFERENCES media(id),
    CONSTRAINT uq_company_media UNIQUE (company_id, media_id)
)
"""

CREATE_INDEXES_SQL_SQLITE = [
    "CREATE INDEX IF NOT EXISTS ix_company_media_company ON company_media(company_id)",
    "CREATE INDEX IF NOT EXISTS ix_company_media_media ON company_media(media_id)",
]


async def main():
    async with engine.begin() as conn:
        dialect = conn.dialect.name
        if dialect.startswith("postgres"):
            await conn.execute(text(CREATE_TABLE_SQL_PG))
            for stmt in CREATE_INDEXES_SQL_PG:
                await conn.execute(text(stmt))
            print("Ensured company_media table exists (Postgres)")
        else:
            await conn.execute(text(CREATE_TABLE_SQL_SQLITE))
            for stmt in CREATE_INDEXES_SQL_SQLITE:
                await conn.execute(text(stmt))
            print("Ensured company_media table exists (SQLite)")


if __name__ == "__main__":
    asyncio.run(main())

