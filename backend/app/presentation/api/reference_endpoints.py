from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.db import get_session
from app.infrastructure.repos.reference_repo import ReferenceRepo
from app.presentation.schemas.profiles import SphereOut, SkillOut, StatusOut
from app.usecases.references import ReferenceUseCase


router = APIRouter()


@router.get("/spheres", response_model=list[SphereOut])
async def list_spheres(session: AsyncSession = Depends(get_session)):
    uc = ReferenceUseCase(refs=ReferenceRepo(session))
    spheres = await uc.list_spheres()
    return [
        SphereOut(id=s.id, title=s.title, background_color=s.background_color, text_color=s.text_color)
        for s in spheres
    ]


@router.get("/skills", response_model=list[SkillOut])
async def list_skills(
    sphere_id: Optional[str] = Query(default=None),
    session: AsyncSession = Depends(get_session),
):
    uc = ReferenceUseCase(refs=ReferenceRepo(session))
    skills = await uc.list_skills(sphere_id=sphere_id)
    return [
        SkillOut(
            id=sk.id,
            title=sk.title,
            sphere=(
                SphereOut(
                    id=sk.sphere.id,
                    title=sk.sphere.title,
                    background_color=sk.sphere.background_color,
                    text_color=sk.sphere.text_color,
                )
                if sk.sphere
                else None
            ),
        )
        for sk in skills
    ]


@router.get("/statuses", response_model=list[StatusOut])
async def list_statuses(session: AsyncSession = Depends(get_session)):
    uc = ReferenceUseCase(refs=ReferenceRepo(session))
    statuses = await uc.list_statuses()
    return [StatusOut(id=st.id, title=st.title) for st in statuses]

