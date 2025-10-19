"""
Add a default case to communities that have no cases yet.

Defaults:
- title: "Умная система управления питанием микрочипа"
- date: 2025-10-17 00:00:00
- solutions_count: 28

Idempotent: only inserts for communities with zero cases.

Run:
  docker compose exec api python -m app.scripts.add_missing_cases

Optional overrides:
  docker compose exec api python -m app.scripts.add_missing_cases \
    --title "Мой кейс" --date 2025-10-17 --solutions 28
"""

from __future__ import annotations

import argparse
import asyncio
import datetime as dt
from typing import Set

from sqlalchemy import select

from app.adapters.db import async_session
from app.infrastructure.repos.sql_models import CommunityModel, CaseModel


async def add_missing_cases(title: str, date: dt.datetime, solutions_count: int) -> None:
    async with async_session() as session:
        # All community IDs
        community_ids = [c for c in (await session.execute(select(CommunityModel.id))).scalars().all()]

        # Community IDs that already have at least one case
        existing_case_comm_ids: Set[str] = set(
            (await session.execute(select(CaseModel.community_id).distinct())).scalars().all()
        )

        # Communities missing cases
        missing = [cid for cid in community_ids if cid not in existing_case_comm_ids]

        to_add = [
            CaseModel(
                community_id=cid,
                title=title,
                description=None,
                date=date,
                solutions_count=solutions_count,
            )
            for cid in missing
        ]

        if to_add:
            session.add_all(to_add)
            await session.commit()
        print(
            f"Communities: {len(community_ids)}; with cases: {len(existing_case_comm_ids)}; "
            f"added default cases: {len(to_add)}"
        )


def _parse_args(argv: list[str] | None = None):
    p = argparse.ArgumentParser(description="Add default case to communities without cases")
    p.add_argument("--title", default="Умная система управления питанием микрочипа")
    p.add_argument("--date", default="2025-10-17", help="YYYY-MM-DD")
    p.add_argument("--solutions", type=int, default=28, help="solutions_count")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    # Parse date
    try:
        date = dt.datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError:
        raise SystemExit("--date must be in YYYY-MM-DD format")
    asyncio.run(add_missing_cases(args.title, date, args.solutions))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

