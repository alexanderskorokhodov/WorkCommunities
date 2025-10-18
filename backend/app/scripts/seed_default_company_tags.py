"""
Set default tags for each company if tags are empty or NULL.

Default tags:
  - IT | Стажировки
  - Роботехника

Usage (Docker):
  docker compose exec api python -m app.scripts.seed_default_company_tags

Idempotent: only updates companies without tags.
"""

import asyncio
from sqlalchemy import select

from app.adapters.db import async_session
from app.infrastructure.repos.sql_models import CompanyModel

DEFAULT_TAGS = ["IT | Стажировки", "Роботехника"]


async def seed_default_company_tags():
    updated = 0
    async with async_session() as session:
        res = await session.execute(select(CompanyModel))
        companies = res.scalars().all()
        for c in companies:
            if c.tags and c.tags.strip():
                continue
            c.tags = ",".join(DEFAULT_TAGS)
            session.add(c)
            updated += 1
        await session.commit()
    print(f"Updated {updated} compan(y|ies) with default tags.")


def main():
    asyncio.run(seed_default_company_tags())


if __name__ == "__main__":
    main()

