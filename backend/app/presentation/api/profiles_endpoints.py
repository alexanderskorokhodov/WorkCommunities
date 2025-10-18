from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.db import get_session
from app.core.deps import get_current_user
from app.infrastructure.repos.profile_repo import ProfileRepo
from app.infrastructure.repos.community_repo import CommunityRepo
from app.infrastructure.repos.event_repo import EventRepo
from app.presentation.schemas.profiles import ProfileOut, ProfileUpdateIn, SkillOut, SphereOut, StatusOut
from app.presentation.schemas.communities import CommunityOut
from app.presentation.schemas.events import EventOut
from app.usecases.profiles import ProfileUseCase

router = APIRouter()


def _to_out(p, *, communities: list[CommunityOut] | None = None, joined_events: list[EventOut] | None = None) -> ProfileOut:
    skills = []
    for sk in p.skills:
        sphere = sk.sphere
        skills.append(SkillOut(
            id=sk.id,
            title=sk.title,
            sphere=(SphereOut(id=sphere.id, title=sphere.title, background_color=sphere.background_color, text_color=sphere.text_color) if sphere else None)
        ))
    statuses = [StatusOut(id=st.id, title=st.title) for st in p.statuses]
    return ProfileOut(
        id=p.id,
        user_id=p.user_id,
        full_name=p.full_name,
        portfolio_url=p.portfolio_url,
        description=p.description,
        skills=skills,
        statuses=statuses,
        communities=communities or [],
        joined_events=joined_events or [],
    )


@router.get("/me", response_model=ProfileOut)
async def get_my_profile(session: AsyncSession = Depends(get_session), user=Depends(get_current_user)):
    uc = ProfileUseCase(profiles=ProfileRepo(session))
    p = await uc.get_or_create_for_user(user.id)
    # Fetch user communities and joined events
    comm_repo = CommunityRepo(session)
    evt_repo = EventRepo(session)
    communities = await comm_repo.list_for_user(user.id)
    joined = await evt_repo.list_joined_for_user(user.id, limit=50)
    communities_out = [
        CommunityOut(
            id=c.id,
            name=c.name,
            company_id=c.company_id,
            description=c.description,
            telegram_url=c.telegram_url,
            tags=c.tags,
            is_archived=c.is_archived,
            logo_media_id=c.logo_media_id,
            members_count=None,
        )
        for c in communities
    ]
    joined_events_out = [
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
        for e in joined
    ]
    return _to_out(p, communities=communities_out, joined_events=joined_events_out)


@router.patch("/me", response_model=ProfileOut)
async def update_my_profile(data: ProfileUpdateIn, session: AsyncSession = Depends(get_session), user=Depends(get_current_user)):
    uc = ProfileUseCase(profiles=ProfileRepo(session))
    try:
        p = await uc.update(user.id, **data.model_dump(exclude_unset=True))
    except ValueError as e:
        # invalid skill/status ids provided
        raise HTTPException(status_code=400, detail=str(e))
    # same enrichment as in GET /me
    comm_repo = CommunityRepo(session)
    evt_repo = EventRepo(session)
    communities = await comm_repo.list_for_user(user.id)
    joined = await evt_repo.list_joined_for_user(user.id, limit=50)
    communities_out = [
        CommunityOut(
            id=c.id,
            name=c.name,
            company_id=c.company_id,
            description=c.description,
            telegram_url=c.telegram_url,
            tags=c.tags,
            is_archived=c.is_archived,
            logo_media_id=c.logo_media_id,
            members_count=None,
        )
        for c in communities
    ]
    joined_events_out = [
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
        for e in joined
    ]
    return _to_out(p, communities=communities_out, joined_events=joined_events_out)
