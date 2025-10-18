from app.domain.repositories import IEventRepo


class EventsUseCase:
    def __init__(self, events: IEventRepo):
        self.events = events

    async def upcoming_for_user(self, user_id: str, limit: int = 20):
        return await self.events.list_for_user(user_id, limit)

    async def my_upcoming(self, user_id: str, limit: int = 20):
        return await self.events.list_joined_for_user(user_id, limit)

    async def upcoming_all(self, limit: int = 20):
        return await self.events.list_all_upcoming(limit)

    async def join(self, user_id: str, event_id: str):
        return await self.events.join(user_id, event_id)

    async def unjoin(self, user_id: str, event_id: str):
        return await self.events.unjoin(user_id, event_id)

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
        tags: list[str] | None = None,
        skill_ids: list[str] | None = None,
        cost: int | None = None,
        participant_payout: int | None = None,
    ):
        return await self.events.create(
            community_id=community_id,
            title=title,
            event_date=event_date,
            city=city,
            location=location,
            description=description,
            registration=registration,
            format=format,
            media_id=media_id,
            tags=tags,
            skill_ids=skill_ids,
            cost=cost,
            participant_payout=participant_payout,
        )
