from app.domain.repositories import IEventRepo


class EventsUseCase:
    def __init__(self, events: IEventRepo):
        self.events = events

    async def upcoming_for_user(self, user_id: str, limit: int = 20):
        return await self.events.list_for_user(user_id, limit)

