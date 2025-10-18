from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import Membership
from app.domain.repositories import IMembershipRepo
from .sql_models import MembershipModel


def _from_row(m: MembershipModel) -> Membership:
    return Membership(id=m.id, user_id=m.user_id, community_id=m.community_id, role=m.role)


class MembershipRepo(IMembershipRepo):
    def __init__(self, s: AsyncSession):
        self.s = s

    async def join(self, user_id: str, community_id: str) -> Membership:
        m = MembershipModel(user_id=user_id, community_id=community_id, role="member")
        self.s.add(m)
        await self.s.flush()
        return _from_row(m)

    async def exit(self, user_id: str, community_id: str) -> None:
        await self.s.execute(
            delete(MembershipModel).where(MembershipModel.user_id == user_id, MembershipModel.community_id == community_id)
        )

    async def list_user_ids_for_community(self, community_id: str) -> list[str]:
        res = await self.s.execute(select(MembershipModel.user_id).where(MembershipModel.community_id == community_id))
        rows = res.scalars().all()
        return list(rows)

    async def counts_for_communities(self, community_ids: list[str]) -> dict[str, int]:
        if not community_ids:
            return {}
        stmt = (
            select(MembershipModel.community_id, func.count(MembershipModel.user_id))
            .where(MembershipModel.community_id.in_(community_ids))
            .group_by(MembershipModel.community_id)
        )
        res = await self.s.execute(stmt)
        rows = res.all()
        return {cid: int(count) for cid, count in rows}
