from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.db import get_session
from app.infrastructure.repos.user_repo import UserRepo
from app.infrastructure.repos.profile_repo import ProfileRepo
from app.infrastructure.repos.community_repo import CommunityRepo
from app.presentation.schemas.users import (
    UserOut,
    UserDetailOut,
    CommunityForUserOut,
    SkillForUserOut,
    StatusForUserOut,
    SphereForUserOut,
)


router = APIRouter()


@router.get("/", response_model=list[UserOut])
async def list_users(session: AsyncSession = Depends(get_session)):
    repo = UserRepo(session)
    users = await repo.list_all()
    return [
        UserOut(
            id=u.id,
            role=u.role,
            phone=u.phone or "",
            email=u.email or "",
            avatar_media_id=u.avatar_media_id or "",
            created_at=u.created_at,
        )
        for u in users
    ]


@router.get("/{user_id}", response_model=UserDetailOut)
async def get_user(user_id: str, session: AsyncSession = Depends(get_session)):
    urepo = UserRepo(session)
    prepo = ProfileRepo(session)
    crepo = CommunityRepo(session)

    u = await urepo.get_by_id(user_id)
    if not u:
        raise HTTPException(404, "Not found")

    prof = await prepo.get_by_user_id(u.id)
    full_name = prof.full_name if prof else None

    comms = await crepo.list_for_user(u.id)

    return UserDetailOut(
        id=u.id,
        role=u.role,
        phone=u.phone or "",
        full_name=full_name,
        portfolio_url=((prof.portfolio_url or "") if prof else ""),
        description=((prof.description or "") if prof else ""),
        skills=[
            SkillForUserOut(
                id=s.id,
                title=s.title,
                sphere=(SphereForUserOut(
                    id=s.sphere.id,
                    title=s.sphere.title,
                    background_color=s.sphere.background_color,
                    text_color=s.sphere.text_color,
                ) if s.sphere else None),
            )
            for s in (prof.skills if prof else [])
        ],
        statuses=[
            StatusForUserOut(id=st.id, title=st.title)
            for st in (prof.statuses if prof else [])
        ],
        avatar_media_id=u.avatar_media_id or "",
        created_at=u.created_at,
        communities=[
            CommunityForUserOut(
                id=c.id,
                company_id=c.company_id,
                name=c.name,
                description=c.description,
                telegram_url=c.telegram_url,
                tags=c.tags,
                is_archived=c.is_archived,
                logo_media_id=c.logo_media_id,
            )
            for c in comms
        ],
    )
