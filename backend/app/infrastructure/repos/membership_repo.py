from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import Membership
from app.domain.repositories import IMembershipRepo
from .sql_models import MembershipModel
from sqlalchemy import select


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
