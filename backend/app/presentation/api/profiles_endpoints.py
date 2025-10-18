from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.db import get_session
from app.core.deps import get_current_user
from app.infrastructure.repos.profile_repo import ProfileRepo
from app.presentation.schemas.profiles import ProfileOut, ProfileUpdateIn, SkillOut, SphereOut, StatusOut
from app.usecases.profiles import ProfileUseCase

router = APIRouter()


def _to_out(p) -> ProfileOut:
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
    )


@router.get("/me", response_model=ProfileOut)
async def get_my_profile(session: AsyncSession = Depends(get_session), user=Depends(get_current_user)):
    uc = ProfileUseCase(profiles=ProfileRepo(session))
    p = await uc.get_or_create_for_user(user.id)
    return _to_out(p)


@router.patch("/me", response_model=ProfileOut)
async def update_my_profile(data: ProfileUpdateIn, session: AsyncSession = Depends(get_session), user=Depends(get_current_user)):
    uc = ProfileUseCase(profiles=ProfileRepo(session))
    try:
        p = await uc.update(user.id, **data.model_dump(exclude_unset=True))
    except ValueError as e:
        # invalid skill/status ids provided
        raise HTTPException(status_code=400, detail=str(e))
    return _to_out(p)
