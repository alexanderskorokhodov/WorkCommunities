import asyncio
from sqlalchemy import select

from app.adapters.db import engine, async_session
from app.infrastructure.repos.sql_models import Base, StatusModel, SphereModel, SkillModel


async def ensure_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_or_create_status(title: str) -> StatusModel:
    async with async_session() as session:
        res = await session.execute(select(StatusModel).where(StatusModel.title == title))
        existing = res.scalar_one_or_none()
        if existing:
            return existing
        s = StatusModel(title=title)
        session.add(s)
        await session.commit()
        await session.refresh(s)
        return s


async def get_or_create_sphere(title: str, background_color: str, text_color: str) -> SphereModel:
    async with async_session() as session:
        res = await session.execute(select(SphereModel).where(SphereModel.title == title))
        existing = res.scalar_one_or_none()
        if existing:
            # update colors if changed
            changed = False
            if existing.background_color != background_color:
                existing.background_color = background_color
                changed = True
            if existing.text_color != text_color:
                existing.text_color = text_color
                changed = True
            if changed:
                await session.commit()
            return existing
        s = SphereModel(title=title, background_color=background_color, text_color=text_color)
        session.add(s)
        await session.commit()
        await session.refresh(s)
        return s


async def get_or_create_skill(title: str, sphere_id: str) -> SkillModel:
    async with async_session() as session:
        res = await session.execute(
            select(SkillModel).where(SkillModel.title == title, SkillModel.sphere_id == sphere_id)
        )
        existing = res.scalar_one_or_none()
        if existing:
            return existing
        sk = SkillModel(title=title, sphere_id=sphere_id)
        session.add(sk)
        await session.commit()
        await session.refresh(sk)
        return sk


async def seed_reference():
    await ensure_tables()

    # Statuses
    status_titles = [
        "Студент",
        "Стажёр",
        "Работаю",
        "Выпускник",
        "Ищу стажировку",
    ]
    for t in status_titles:
        await get_or_create_status(t)

    # Spheres and skills
    # Bio sphere
    bio = await get_or_create_sphere(
        title="Био",
        background_color="#E5F7DB",
        text_color="#308414",
    )
    for sk_title in [
        "Биотех",
        "Хим. инженерия",
        "ХимТех",
    ]:
        await get_or_create_skill(sk_title, bio.id)

    # IT sphere (text: #2AABEE, background: #CDEEFF)
    it = await get_or_create_sphere(
        title="IT",
        background_color="#CDEEFF",
        text_color="#2AABEE",
    )
    for sk_title in [
        "Тестирование",
        "Робототехника",
        "Инженерия",
        "Информационная безопасность",
        "Html/css",
        "Go/React",
    ]:
        await get_or_create_skill(sk_title, it.id)

    print("Reference data seeded: statuses, spheres, skills.")


def main():
    asyncio.run(seed_reference())


if __name__ == "__main__":
    main()

