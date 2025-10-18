from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import Follow
from app.domain.repositories import IFollowRepo
from .sql_models import FollowModel


def _from_row(m: FollowModel) -> Follow:
    return Follow(id=m.id, user_id=m.user_id, community_id=m.community_id)


class FollowRepo(IFollowRepo):
    def __init__(self, s: AsyncSession):
        self.s = s

    async def follow(self, user_id: str, community_id: str) -> Follow:
        m = FollowModel(user_id=user_id, community_id=community_id)
        self.s.add(m)
        await self.s.flush()
        return _from_row(m)

    async def unfollow(self, user_id: str, community_id: str) -> None:
        await self.s.execute(
            delete(FollowModel).where(FollowModel.user_id == user_id, FollowModel.community_id == community_id)
        )

    async def list_community_ids_for_user(self, user_id: str) -> list[str]:
        res = await self.s.execute(select(FollowModel.community_id).where(FollowModel.user_id == user_id))
        return [r for r, in res.all()]
