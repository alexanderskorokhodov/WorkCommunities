import asyncio

from app.adapters.db import engine
from app.infrastructure.repos.sql_models import Base


async def drop_and_recreate():
    async with engine.begin() as conn:
        # Drop all tables then recreate empty schema
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


def main():
    asyncio.run(drop_and_recreate())
    print("Database schema dropped and recreated (empty).")


if __name__ == "__main__":
    main()

