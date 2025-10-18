from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.db import get_session
from app.core.deps import get_current_user
from app.infrastructure.repos.event_repo import EventRepo
from app.presentation.schemas.events import EventOut
from app.usecases.events import EventsUseCase

router = APIRouter()


@router.get("/upcoming", response_model=list[EventOut])
async def list_upcoming(limit: int = 20, session: AsyncSession = Depends(get_session), user=Depends(get_current_user)):
    uc = EventsUseCase(events=EventRepo(session))
    events = await uc.upcoming_for_user(user.id, limit=limit)
    return [EventOut(id=e.id, community_id=e.community_id, title=e.title, starts_at=e.starts_at, city=e.city) for e in events]

