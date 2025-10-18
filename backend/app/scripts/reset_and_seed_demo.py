"""
Reset DB content (keep spheres/skills/statuses) and seed demo data.

Actions:
- Wipe users, profiles, companies, communities, content (posts/events), stories, media,
  memberships, follows, company follows, media relations, cases, OTPs — but keep
  reference tables: spheres, skills, statuses.
- Upload all images from a media directory via HTTP endpoint to obtain media IDs.
- Seed users with profiles (using existing skills/statuses), companies with logos,
  communities with logos, a post, and events linking uploaded media.

Usage:
  python -m app.scripts.reset_and_seed_demo --base-url http://localhost:8000 \
      --media-dir app/scripts/media_mockups

Notes:
- Requires the API server running and accessible at --base-url for media upload.
- No authentication is required for /media/upload in this codebase.
"""

from __future__ import annotations

import argparse
import asyncio
import datetime as dt
import io
import os
from typing import Dict

import requests
from sqlalchemy import text, select, update, delete

from app.adapters.db import engine, async_session
from app.infrastructure.repos.sql_models import (
    Base,
    UserModel,
    ProfileModel,
    CompanyModel,
    CommunityModel,
    ContentModel,
    StoryModel,
    MediaModel,
    ContentMediaModel,
    CompanyMediaModel,
    ContentSkillModel,
    EventParticipantModel,
    FollowModel,
    CompanyFollowModel,
    MembershipModel,
    ProfileSkillModel,
    ProfileStatusModel,
    CaseModel,
    StatusModel,
    SkillModel,
)
from app.infrastructure.repos.user_repo import UserRepo
from app.infrastructure.repos.profile_repo import ProfileRepo
from app.infrastructure.repos.company_repo import CompanyRepo
from app.infrastructure.repos.community_repo import CommunityRepo
from app.infrastructure.repos.post_repo import PostRepo
from app.infrastructure.repos.event_repo import EventRepo
from app.infrastructure.repos.case_repo import CaseRepo


def _log(msg: str) -> None:
    print(msg)


async def ensure_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def migrate_add_company_phone_column() -> None:
    """Ensure companies.phone column exists (safe for old DBs)."""
    async with engine.begin() as conn:
        try:
            await conn.execute(text("ALTER TABLE companies ADD COLUMN IF NOT EXISTS phone varchar"))
            await conn.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS uq_companies_phone ON companies(phone)"))
        except Exception:
            # Best-effort; ignore if DB variant doesn't support IF NOT EXISTS
            pass


async def clear_db_keep_refs() -> None:
    """Delete rows from content tables, preserving spheres/skills/statuses."""
    async with engine.begin() as conn:
        async def _safe_delete(tablename: str):
            try:
                await conn.execute(text(f"DELETE FROM {tablename}"))
            except Exception:
                # table may not exist in this DB (legacy/new mix) — ignore
                pass
        # Order matters due to FKs
        for table in [
            # dependents first
            EventParticipantModel.__table__,
            ContentSkillModel.__table__,
            ContentMediaModel.__table__,
            CompanyMediaModel.__table__,
            FollowModel.__table__,
            CompanyFollowModel.__table__,
            MembershipModel.__table__,
            ProfileSkillModel.__table__,
            ProfileStatusModel.__table__,
            StoryModel.__table__,
            CaseModel.__table__,
            ContentModel.__table__,
            # try legacy tables before communities
            # legacy link table for post->media
            # these are best-effort and may be absent
        ]:
            await conn.execute(delete(table))
        # legacy tables clean up
        await _safe_delete("post_media")
        await _safe_delete("posts")
        await _safe_delete("events")
        # continue with entities that depend on communities/companies/users
        for table in [
            CommunityModel.__table__,
            CompanyModel.__table__,
            ProfileModel.__table__,
            UserModel.__table__,
            MediaModel.__table__,
        ]:
            await conn.execute(delete(table))
        # Also clear OTPs if present
        await conn.execute(text("DELETE FROM otps"))


def upload_media_dir(base_url: str, media_dir: str) -> Dict[str, str]:
    """Upload all files in media_dir to /media/upload, return {filename: media_id}."""
    mapping: Dict[str, str] = {}
    url = base_url.rstrip("/") + "/media/upload"
    for name in sorted(os.listdir(media_dir)):
        path = os.path.join(media_dir, name)
        if not os.path.isfile(path):
            continue
        mime = _guess_mime(name)
        with open(path, "rb") as f:
            files = {"file": (name, io.BytesIO(f.read()), mime)}
            r = requests.post(url, files=files, timeout=60)
        if r.status_code != 200:
            raise RuntimeError(f"Upload failed for {name}: {r.status_code} {r.text}")
        mid = r.json().get("id")
        if not mid:
            raise RuntimeError(f"Upload returned no id for {name}")
        mapping[name] = mid
        _log(f"Uploaded {name} -> {mid}")
    return mapping


def _guess_mime(name: str) -> str:
    ext = os.path.splitext(name)[1].lower()
    return {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
    }.get(ext, "application/octet-stream")


async def seed_users(session, media_map: Dict[str, str]) -> None:
    """Create users and profiles; set avatar for the first user."""
    user_repo = UserRepo(session)
    profile_repo = ProfileRepo(session)

    description = (
        "Меня увлекает задача превращать сложные расчеты и инженерные расчеты в реальные, работающие механизмы. За время учебы и проектной работы я углубленно освоила SolidWorks, AutoCAD и ANSYS, что подтверждается моими дипломными проектами и победами на университетских конкурсах.\n\n"
        "Мой ключевой проект — разработка и оптимизация узла гидравлической системы, где мне удалось на 15% снизить массу конструкции без потери прочностных характеристик. Этот опыт научи меня не только виртуозному владению ПО, но и принципам проектирования, ориентированного на эффективность и стоимость.\n\n"
        "Я ищу возможность применить свои навыки в вашей компании, чтобы внести свой вклад в решение практических задач и учиться у лучших специалистов отрасли. Открыта к предложениям о стажировке и работе в сфере машиностроения, аэрокосмической промышленности или энергетики."
    )

    names = [
        "Ксения Хакатонова",
        "Платон Максимов",
        "Фёдор Морозов",
        "Марианна Нестерова",
        "Мирон Грачев",
        "Максим Давыдов",
        "Юрий Афанасьев",
    ]

    # Resolve skills by title
    res_sk = await session.execute(select(SkillModel))
    skills = {s.title: s.id for s in res_sk.scalars().all()}
    sk_biotech = skills.get("Биотех")
    sk_chemeng = skills.get("Хим. инженерия")

    # Resolve status 'Студент'
    res_st = await session.execute(select(StatusModel).where(StatusModel.title == "Студент"))
    st_student = res_st.scalar_one_or_none()
    status_ids = [st_student.id] if st_student else []

    for idx, full_name in enumerate(names):
        phone = f"+7999123{idx:03d}"
        u = await user_repo.create_student(phone=phone)
        _log(f"Created user: id={u.id}, role={u.role}, phone={u.phone}, email={u.email}, avatar_media_id={u.avatar_media_id}")
        p = await profile_repo.update(
            u.id,
            full_name=full_name,
            description=description,
            skill_uids=[sid for sid in [sk_biotech, sk_chemeng] if sid] if idx == 0 else None,
            status_uids=status_ids,
        )
        _log(f"Updated profile: user_id={u.id}, full_name={full_name}")
        # Set avatar for the first user
        if idx == 0 and "avatar1.png" in media_map:
            await session.execute(update(UserModel).where(UserModel.id == u.id).values(avatar_media_id=media_map["avatar1.png"]))
            _log(f"Set avatar for user {u.id}: media_id={media_map['avatar1.png']}")
    await session.flush()


async def seed_companies_and_communities(session, media_map: Dict[str, str]) -> dict:
    """Create companies and communities, set logos; return dict with ids."""
    company_repo = CompanyRepo(session)
    community_repo = CommunityRepo(session)

    # Company 1: АО «Микрон»
    desc_mikron = (
        "Инженерия из скилов. Ведущий центр микроэлектроники, где рождаются технологии будущего.\n\n"
        "Компания занимается разработкой и производством чипов, RFID-меток, сенсоров и решений для “умного” мира — от банковских карт до систем безопасности и интернета вещей.\n\n"
        "Мы объединяем инженеров, разработчиков и дизайнеров, чтобы создавать реальные продукты."
    )
    c1 = await company_repo.create(name="АО «Микрон»", description=desc_mikron, phone="+79990000001")
    if "logo1.png" in media_map:
        c1 = await company_repo.update(c1.id, logo_media_id=media_map["logo1.png"])
    _log(f"Created company: id={c1.id}, name={c1.name}, phone={c1.phone}, logo_media_id={c1.logo_media_id}")

    # Assign tags for АО «Микрон» by skill IDs: Биотех + Хим. инженерия
    res_sk = await session.execute(select(SkillModel))
    skills = {s.title: s.id for s in res_sk.scalars().all()}
    tag_ids = []
    for t in ["Биотех", "Хим. инженерия"]:
        sid = skills.get(t)
        if sid:
            tag_ids.append(sid)
    if tag_ids:
        c1 = await company_repo.update(c1.id, tags=tag_ids)
        _log(f"Updated company tags for {c1.name}: {c1.tags}")

    comm1 = await community_repo.create(
        name="ИИ и встраиваемые системы",
        company_id=c1.id,
        description="Исследуем и создаём интеллектуальные решения на базе микрочипов и IoT.",
        logo_media_id=media_map.get("community1.png"),
    )
    _log(f"Created community: id={comm1.id}, company_id={comm1.company_id}, name={comm1.name}, logo_media_id={comm1.logo_media_id}")
    comm3 = await community_repo.create(
        name="Проектирование и сборка",
        company_id=c1.id,
        description="Проектирование хим. соединений, погружение в фармацевтику",
        logo_media_id=media_map.get("community3.png"),
    )
    _log(f"Created community: id={comm3.id}, company_id={comm3.company_id}, name={comm3.name}, logo_media_id={comm3.logo_media_id}")

    # Company 2: R-Pharm
    desc_rpharm = (
        "Ведущий центр микроэлектроники, где рождаются технологии будущего.\n\n"
        "Компания занимается разработкой и производством чипов, RFID-меток, сенсоров и решений для “умного” мира — от банковских карт до систем безопасности и интернета вещей.\n\n"
        "Мы объединяем инженеров, разработчиков и дизайнеров, чтобы создавать реальные продукты."
    )
    c2 = await company_repo.create(name="R-Pharm", description=desc_rpharm, phone="+79990000002")
    if "logo2.png" in media_map:
        c2 = await company_repo.update(c2.id, logo_media_id=media_map["logo2.png"])
    _log(f"Created company: id={c2.id}, name={c2.name}, phone={c2.phone}, logo_media_id={c2.logo_media_id}")

    comm2 = await community_repo.create(
        name="Химическая инженерия",
        company_id=c2.id,
        description="Проектирование хим. соединений, погружение в фармацевтику",
        logo_media_id=media_map.get("community2.png"),
    )
    _log(f"Created community: id={comm2.id}, company_id={comm2.company_id}, name={comm2.name}, logo_media_id={comm2.logo_media_id}")

    return {
        "companies": {"mikron": c1.id, "rpharm": c2.id},
        "communities": {"c1": comm1.id, "c2": comm2.id, "c3": comm3.id},
    }


async def seed_cases(session, ids: dict) -> None:
    """Seed requested case into community 'Проектирование и сборка' (c3)."""
    case_repo = CaseRepo(session)
    title = "Умная система управления питанием микрочипа"
    date = dt.datetime(2025, 10, 17, 0, 0, 0)
    cs = await case_repo.create(
        community_id=ids["communities"]["c3"],
        title=title,
        description=None,
        date=date,
        solutions_count=28,
    )
    _log(f"Created case: title={cs.title}, community_id={cs.community_id}, date={cs.date}, solutions_count={cs.solutions_count}")


async def seed_post(session, ids: dict, media_map: Dict[str, str]) -> None:
    post_repo = PostRepo(session)
    title = "Как рождается микрочип"
    body = "Краткий обзор этапов производства микрочипов: проектирование, фотолитография, травление и сборка."
    media_ids = [media_map["post1.png"]] if "post1.png" in media_map else []
    post = await post_repo.create(
        community_id=ids["communities"]["c3"],
        title=title,
        body=body,
        media_ids=media_ids,
        tags=None,
        skill_ids=None,
    )
    _log(f"Created post: title={title}, community_id={ids['communities']['c3']}, media_count={len(media_ids)}")


async def seed_events(session, ids: dict, media_map: Dict[str, str]) -> None:
    event_repo = EventRepo(session)

    # Resolve skill 'Инженерия'
    res_sk = await session.execute(select(SkillModel).where(SkillModel.title == "Инженерия"))
    sk_engineering = res_sk.scalar_one_or_none()
    sk_ids = [sk_engineering.id] if sk_engineering else None

    # Dates
    d1 = dt.datetime(2025, 10, 22, 12, 0, 0)
    d2 = dt.datetime(2025, 10, 24, 12, 0, 0)
    d3 = dt.datetime(2025, 10, 25, 12, 0, 0)
    d4 = dt.datetime(2025, 10, 24, 17, 0, 0)

    e1 = await event_repo.create(
        community_id=ids["communities"]["c1"],
        title="Хакатон «BioData Hack»",
        event_date=d1,
        city=None,
        location=None,
        description=None,
        registration=None,
        format=None,
        media_id=media_map.get("event1.png"),
        tags=None,
        skill_ids=None,
        cost=100,
        participant_payout=None,
    )

    e2 = await event_repo.create(
        community_id=ids["communities"]["c2"],
        title="Воркшоп «Схемотехника для начинающих»",
        event_date=d2,
        city=None,
        location=None,
        description=None,
        registration=None,
        format=None,
        media_id=media_map.get("event2.png"),
        tags=None,
        skill_ids=sk_ids,
        cost=None,
        participant_payout=None,
    )

    e3 = await event_repo.create(
        community_id=ids["communities"]["c2"],
        title="Вебинар «3 навыка, которые …»",
        event_date=d3,
        city=None,
        location=None,
        description=None,
        registration=None,
        format=None,
        media_id=media_map.get("event3.png"),
        tags=None,
        skill_ids=sk_ids,
        cost=10,
        participant_payout=None,
    )

    e4 = await event_repo.create(
        community_id=ids["communities"]["c2"],
        title="Онлайн-воркшоп от R-Pharm с Василием Игнатьевым",
        event_date=d4,
        city=None,
        location=None,
        description=(
            "Уже в эту пятницу приглашаем на встречу с Василием Игнатьевым, экспертом R-Farm по биотехнологическим инновациям.\n\n"
            "Разберём реальные кейсы из индустрии, поговорим о карьере в фарме и разложим по полочкам, как молодым специалистам попасть в проекты R-Farm."
        ),
        registration="в сообществе R-Farm BioTech Club",
        format="открытая сессия + ответы на вопросы",
        media_id=media_map.get("event0.png"),
        tags=None,
        skill_ids=None,
        cost=None,
        participant_payout=5,
    )


async def run(base_url: str, media_dir: str) -> None:
    await ensure_tables()
    # Ensure cases table and columns are compatible with current code
    # 1) Create table/index if needed; 2) Rename legacy 'points' -> 'solutions_count'
    from app.scripts.migrate_add_cases_table import _ensure_table_and_index, _migrate_points_to_solutions_count  # type: ignore
    async with engine.begin() as conn:
        flavor = await _ensure_table_and_index(conn)
        await _migrate_points_to_solutions_count(conn, flavor)
    # Lightweight migration to add companies.phone if missing
    await migrate_add_company_phone_column()
    _log("Clearing DB (keeping references)...")
    await clear_db_keep_refs()
    _log("Uploading media...")
    media_map = upload_media_dir(base_url, media_dir)
    _log("Seeding data...")
    async with async_session() as session:
        # Users
        await seed_users(session, media_map)
        # Companies/Communities
        ids = await seed_companies_and_communities(session, media_map)
        # Post
        await seed_post(session, ids, media_map)
        # Events
        await seed_events(session, ids, media_map)
        # Cases
        await seed_cases(session, ids)
        await session.commit()
    _log("Done: demo data seeded.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Reset DB and seed demo data")
    parser.add_argument("--base-url", default="http://localhost:8000", help="Service base URL")
    parser.add_argument("--media-dir", default="app/scripts/media_mockups", help="Directory with images to upload")
    args = parser.parse_args(argv)

    asyncio.run(run(args.base_url, args.media_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
    for e in [e1, e2, e3, e4]:
        _log(f"Created event: title={e.title}, community_id={e.community_id}, date={e.event_date}")
