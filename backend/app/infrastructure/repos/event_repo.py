from datetime import datetime
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import Event
from app.domain.repositories import IEventRepo
from .sql_models import EventModel, MembershipModel, FollowModel


def _from_row(m: EventModel) -> Event:
    return Event(id=m.id, community_id=m.community_id, title=m.title, starts_at=m.starts_at, city=m.city)


class EventRepo(IEventRepo):
    def __init__(self, s: AsyncSession):
        self.s = s

    async def list_for_user(self, user_id: str, limit: int = 20) -> Sequence[Event]:
        now = datetime.utcnow()
        # события в сообществах, где пользователь состоит или за которыми следует
        member_communities = select(MembershipModel.community_id).where(MembershipModel.user_id == user_id)
        follow_communities = select(FollowModel.community_id).where(FollowModel.user_id == user_id)
        stmt = (
            select(EventModel)
            .where(
                EventModel.starts_at >= now,
                EventModel.community_id.in_(member_communities.union_all(follow_communities)),
            )
            .order_by(EventModel.starts_at.asc())
            .limit(limit)
        )
        res = await self.s.execute(stmt)
        return [_from_row(r) for r in res.scalars().all()]

