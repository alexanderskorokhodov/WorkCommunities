from datetime import datetime
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import Event, EventParticipant
from app.domain.repositories import IEventRepo
from .sql_models import ContentModel, MembershipModel, FollowModel, EventParticipantModel, ContentSkillModel, SkillModel
from sqlalchemy import delete


def _from_row(m: ContentModel) -> Event:
    return Event(
        id=m.id,
        community_id=m.community_id,
        title=m.title,
        event_date=m.event_date,
        city=m.city,
        location=m.location,
        description=m.description,
        registration=m.registration,
        format=m.format,
        media_id=m.media_id,
        tags=[t.strip() for t in (m.tags or "").split(",") if t.strip()],
        cost=m.cost,
        participant_payout=m.participant_payout,
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
            select(ContentModel)
            .where(
                ContentModel.type == "event",
                ContentModel.event_date >= now,
                ContentModel.community_id.in_(member_communities.union_all(follow_communities)),
            )
            .order_by(ContentModel.event_date.asc())
            .limit(limit)
        )
        res = await self.s.execute(stmt)
        return [_from_row(r) for r in res.scalars().all()]

    async def list_joined_for_user(self, user_id: str, limit: int = 20) -> Sequence[Event]:
        now = datetime.utcnow()
        # события, на которые пользователь зарегистрирован
        joined_event_ids = select(EventParticipantModel.content_id).where(EventParticipantModel.user_id == user_id)
        stmt = (
            select(ContentModel)
            .where(ContentModel.id.in_(joined_event_ids), ContentModel.event_date >= now, ContentModel.type == "event")
            .order_by(ContentModel.event_date.asc())
            .limit(limit)
        )
        res = await self.s.execute(stmt)
        return [_from_row(r) for r in res.scalars().all()]

    async def list_all_upcoming(self, limit: int = 20) -> Sequence[Event]:
        now = datetime.utcnow()
        stmt = (
            select(ContentModel)
            .where(ContentModel.type == "event", ContentModel.event_date >= now)
            .order_by(ContentModel.event_date.asc())
            .limit(limit)
        )
        res = await self.s.execute(stmt)
        return [_from_row(r) for r in res.scalars().all()]

    async def create(
        self,
        *,
        community_id: str,
        title: str,
        event_date,
        city: str | None = None,
        location: str | None = None,
        description: str | None = None,
        registration: str | None = None,
        format: str | None = None,
        media_id: str | None = None,
        tags: Sequence[str] | None = None,
        skill_ids: Sequence[str] | None = None,
        cost: int | None = None,
        participant_payout: int | None = None,
    ) -> Event:
        m = ContentModel(
            community_id=community_id,
            type="event",
            title=title,
            event_date=event_date,
            city=city,
            location=location,
            description=description,
            registration=registration,
            format=format,
            media_id=media_id,
            tags=",".join(tags) if tags else None,
            cost=cost,
            participant_payout=participant_payout,
            created_at=datetime.utcnow(),
        )
        self.s.add(m)
        await self.s.flush()

        if skill_ids:
            for sid in skill_ids:
                self.s.add(ContentSkillModel(content_id=m.id, skill_id=sid))
            await self.s.flush()

        return _from_row(m)

    async def join(self, user_id: str, event_id: str) -> EventParticipant:
        # idempotent join: return existing if already joined
        res = await self.s.execute(
            select(EventParticipantModel).where(
                EventParticipantModel.user_id == user_id, EventParticipantModel.content_id == event_id
            )
        )
        existing = res.scalars().first()
        if existing:
            return EventParticipant(id=existing.id, user_id=existing.user_id, event_id=existing.content_id)

        m = EventParticipantModel(user_id=user_id, content_id=event_id)
        self.s.add(m)
        await self.s.flush()
        return EventParticipant(id=m.id, user_id=m.user_id, event_id=m.content_id)

    async def unjoin(self, user_id: str, event_id: str) -> None:
        await self.s.execute(
            delete(EventParticipantModel).where(
                EventParticipantModel.user_id == user_id, EventParticipantModel.content_id == event_id
            )
        )
