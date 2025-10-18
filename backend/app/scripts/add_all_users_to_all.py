"""
Add all users to all communities and companies.

- Communities: create Membership rows (user_id, community_id)
- Companies: create CompanyFollow rows (user_id, company_id)

Idempotent: skips existing pairs to avoid duplicates.

Run:
  docker compose exec api python -m app.scripts.add_all_users_to_all
"""

import asyncio
from typing import Set, Tuple

from sqlalchemy import select

from app.adapters.db import async_session
from app.infrastructure.repos.sql_models import (
    UserModel,
    CommunityModel,
    CompanyModel,
    MembershipModel,
    CompanyFollowModel,
)


async def add_all_users_to_all():
    async with async_session() as session:
        # Load IDs
        user_ids = [u for u in (await session.execute(select(UserModel.id))).scalars().all()]
        community_ids = [c for c in (await session.execute(select(CommunityModel.id))).scalars().all()]
        company_ids = [c for c in (await session.execute(select(CompanyModel.id))).scalars().all()]

        # Existing memberships (user_id, community_id)
        existing_m_pairs: Set[Tuple[str, str]] = set(
            (uid, cid)
            for uid, cid in (await session.execute(select(MembershipModel.user_id, MembershipModel.community_id))).all()
        )

        # Existing company follows (user_id, company_id)
        existing_f_pairs: Set[Tuple[str, str]] = set(
            (uid, cid)
            for uid, cid in (await session.execute(select(CompanyFollowModel.user_id, CompanyFollowModel.company_id))).all()
        )

        # Prepare new membership rows
        new_memberships = []
        for uid in user_ids:
            for cid in community_ids:
                if (uid, cid) not in existing_m_pairs:
                    new_memberships.append(MembershipModel(user_id=uid, community_id=cid, role="member"))

        # Prepare new company follow rows
        new_follows = []
        for uid in user_ids:
            for coid in company_ids:
                if (uid, coid) not in existing_f_pairs:
                    new_follows.append(CompanyFollowModel(user_id=uid, company_id=coid))

        # Insert
        if new_memberships:
            session.add_all(new_memberships)
        if new_follows:
            session.add_all(new_follows)

        await session.commit()

        print(
            f"Done. Users: {len(user_ids)}, Communities: {len(community_ids)}, Companies: {len(company_ids)}. "
            f"Added memberships: {len(new_memberships)}, company follows: {len(new_follows)}."
        )


def main():
    asyncio.run(add_all_users_to_all())


if __name__ == "__main__":
    main()

