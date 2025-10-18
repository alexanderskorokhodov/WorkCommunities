"""
Lightweight migration for company phone-based auth support:
- Ensure companies.owner_user_id column exists and is indexed
- Ensure users.phone has a unique index (login by phone)

Run: python -m app.scripts.migrate_company_phone_auth
"""

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


async def run():
    async with engine.begin() as conn:
        dialect = conn.dialect.name
        is_pg = dialect.startswith("postgres")

        # companies.owner_user_id
        if is_pg:
            if not await _pg_has_column(conn, "companies", "owner_user_id"):
                await conn.execute(text("ALTER TABLE companies ADD COLUMN owner_user_id VARCHAR NULL"))
                await conn.execute(text("CREATE INDEX IF NOT EXISTS ix_companies_owner_user_id ON companies (owner_user_id)"))
        else:
            if not await _sqlite_has_column(conn, "companies", "owner_user_id"):
                await conn.execute(text("ALTER TABLE companies ADD COLUMN owner_user_id TEXT NULL"))
                await conn.execute(text("CREATE INDEX IF NOT EXISTS ix_companies_owner_user_id ON companies (owner_user_id)"))

        # users.phone unique index (login identifier)
        # Note: column likely exists; we create a unique index defensively.
        if is_pg:
            await conn.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS uq_users_phone ON users (phone)"))
        else:
            await conn.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS uq_users_phone ON users (phone)"))


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()

