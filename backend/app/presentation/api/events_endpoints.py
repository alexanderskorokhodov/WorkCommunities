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
            event_date=e.event_date,
            city=e.city,
            location=e.location,
            description=e.description,
            registration=e.registration,
            format=e.format,
            media_id=e.media_id,
            tags=e.tags,
            # skills are not eagerly loaded here; keeping empty list by default
            cost=e.cost,
            participant_payout=e.participant_payout,
        )
        for e in events
    ]


@router.get("/my/upcoming", response_model=list[EventOut])
async def list_my_upcoming(limit: int = 20, session: AsyncSession = Depends(get_session), user=Depends(get_current_user)):
    uc = EventsUseCase(events=EventRepo(session))
    events = await uc.my_upcoming(user.id, limit=limit)
    return [
        EventOut(
            id=e.id,
            community_id=e.community_id,
            title=e.title,
            event_date=e.event_date,
            city=e.city,
            location=e.location,
            description=e.description,
            registration=e.registration,
            format=e.format,
            media_id=e.media_id,
            tags=e.tags,
            cost=e.cost,
            participant_payout=e.participant_payout,
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
        event_date=data.event_date,
        city=data.city,
        location=data.location,
        description=data.description,
        registration=data.registration,
        format=data.format,
        media_id=data.media_id,
        tags=data.tags,
        skill_ids=data.skill_ids,
        cost=data.cost,
        participant_payout=data.participant_payout,
    )
    return EventOut(
        id=e.id,
        community_id=e.community_id,
        title=e.title,
        event_date=e.event_date,
        city=e.city,
        location=e.location,
        description=e.description,
        registration=e.registration,
        format=e.format,
        media_id=e.media_id,
        tags=e.tags,
        cost=e.cost,
        participant_payout=e.participant_payout,
    )


@router.post("/{event_id}/join")
async def join_event(event_id: str, session: AsyncSession = Depends(get_session), user=Depends(get_current_user)):
    uc = EventsUseCase(events=EventRepo(session))
    await uc.join(user.id, event_id)
    return {"status": "ok"}
