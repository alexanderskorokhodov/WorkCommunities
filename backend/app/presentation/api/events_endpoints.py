from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.db import get_session
from app.core.deps import get_current_user, role_required
from app.infrastructure.repos.event_repo import EventRepo
from app.presentation.schemas.events import EventOut, EventCreateIn
from app.usecases.events import EventsUseCase

router = APIRouter()


@router.get("/upcoming", response_model=list[EventOut])
async def list_upcoming(limit: int = 20, session: AsyncSession = Depends(get_session), user=Depends(get_current_user)):
    uc = EventsUseCase(events=EventRepo(session))
    events = await uc.upcoming_for_user(user.id, limit=limit)
    return [
        EventOut(
            id=e.id,
            community_id=e.community_id,
            title=e.title,
            starts_at=e.starts_at,
            city=e.city,
            location=e.location,
            description=e.description,
            registration=e.registration,
            format=e.format,
            media_id=e.media_id,
        )
        for e in events
    ]


@router.post("/", response_model=EventOut)
async def create_event(data: EventCreateIn, session: AsyncSession = Depends(get_session),
                       user=Depends(role_required("company"))):
    uc = EventsUseCase(events=EventRepo(session))
    e = await uc.create(
        community_id=data.community_id,
        title=data.title,
        starts_at=data.starts_at,
        city=data.city,
        location=data.location,
        description=data.description,
        registration=data.registration,
        format=data.format,
        media_id=data.media_id,
    )
    return EventOut(
        id=e.id,
        community_id=e.community_id,
        title=e.title,
        starts_at=e.starts_at,
        city=e.city,
        location=e.location,
        description=e.description,
        registration=e.registration,
        format=e.format,
        media_id=e.media_id,
    )
