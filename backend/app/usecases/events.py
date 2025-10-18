from app.domain.repositories import IEventRepo


class EventsUseCase:
    def __init__(self, events: IEventRepo):
        self.events = events

    async def upcoming_for_user(self, user_id: str, limit: int = 20):
        return await self.events.list_for_user(user_id, limit)

    async def my_upcoming(self, user_id: str, limit: int = 20):
        return await self.events.list_joined_for_user(user_id, limit)

    async def join(self, user_id: str, event_id: str):
        return await self.events.join(user_id, event_id)

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
    ):
        return await self.events.create(
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
