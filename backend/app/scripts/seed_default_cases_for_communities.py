"""
Create a default Case for each community that doesn't have cases yet.

Usage (Docker):
  docker compose exec api python -m app.scripts.seed_default_cases_for_communities

Idempotent: creates only missing default cases.
"""

import asyncio
from datetime import datetime
import uuid

from sqlalchemy import select

from app.adapters.db import async_session, engine
from app.infrastructure.repos.sql_models import Base, CommunityModel, CaseModel


def _uid() -> str:
    return uuid.uuid4().hex


async def ensure_cases_table():
    # Ensure tables exist (non-destructive). Relies on SQLAlchemy metadata.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def seed_defaults():
    created = 0
    async with async_session() as session:
        res = await session.execute(select(CommunityModel))
        communities = res.scalars().all()
        for c in communities:
            # Check if community already has any case
            res_cases = await session.execute(select(CaseModel).where(CaseModel.community_id == c.id))
            has_case = res_cases.first() is not None
            if has_case:
                continue

            m = CaseModel(
                id=_uid(),
                community_id=c.id,
                title="Стартовый кейс",
                description="Автоматически созданный кейс по умолчанию",
                date=datetime.utcnow(),
                points=0,
            )
            session.add(m)
            created += 1

        await session.commit()
    print(f"Created {created} default case(s) for communities without cases.")


async def main():
    await ensure_cases_table()
    await seed_defaults()


if __name__ == "__main__":
    asyncio.run(main())

