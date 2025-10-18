from app.domain.repositories import IEventRepo


class EventsUseCase:
    def __init__(self, events: IEventRepo):
        self.events = events

    async def upcoming_for_user(self, user_id: str, limit: int = 20):
        return await self.events.list_for_user(user_id, limit)

    async def create(self, *, community_id: str, title: str, starts_at, city: str | None = None):
        return await self.events.create(community_id=community_id, title=title, starts_at=starts_at, city=city)
