from datetime import datetime
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import Event, EventParticipant
from app.domain.repositories import IEventRepo
from .sql_models import EventModel, MembershipModel, FollowModel, EventParticipantModel


def _from_row(m: EventModel) -> Event:
    return Event(
        id=m.id,
        community_id=m.community_id,
        title=m.title,
        starts_at=m.starts_at,
        city=m.city,
        location=m.location,
        description=m.description,
        registration=m.registration,
        format=m.format,
        media_id=m.media_id,
    )


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

    async def list_joined_for_user(self, user_id: str, limit: int = 20) -> Sequence[Event]:
        now = datetime.utcnow()
        # события, на которые пользователь зарегистрирован
        joined_event_ids = select(EventParticipantModel.event_id).where(EventParticipantModel.user_id == user_id)
        stmt = (
            select(EventModel)
            .where(EventModel.id.in_(joined_event_ids), EventModel.starts_at >= now)
            .order_by(EventModel.starts_at.asc())
            .limit(limit)
        )
        res = await self.s.execute(stmt)
        return [_from_row(r) for r in res.scalars().all()]

    async def create(
        self,
        *,
        community_id: str,
        title: str,
        starts_at,
        city: str | None = None,
        location: str | None = None,
        description: str | None = None,
        registration: str | None = None,
        format: str | None = None,
        media_id: str | None = None,
    ) -> Event:
        m = EventModel(
            community_id=community_id,
            title=title,
            starts_at=starts_at,
            city=city,
            location=location,
            description=description,
            registration=registration,
            format=format,
            media_id=media_id,
        )
        self.s.add(m)
        await self.s.flush()
        return _from_row(m)

    async def join(self, user_id: str, event_id: str) -> EventParticipant:
        # idempotent join: return existing if already joined
        res = await self.s.execute(
            select(EventParticipantModel).where(
                EventParticipantModel.user_id == user_id, EventParticipantModel.event_id == event_id
            )
        )
        existing = res.scalars().first()
        if existing:
            return EventParticipant(id=existing.id, user_id=existing.user_id, event_id=existing.event_id)

        m = EventParticipantModel(user_id=user_id, event_id=event_id)
        self.s.add(m)
        await self.s.flush()
        return EventParticipant(id=m.id, user_id=m.user_id, event_id=m.event_id)
