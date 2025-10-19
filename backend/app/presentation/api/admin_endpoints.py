from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.db import get_session
from app.core.deps import role_required
from app.infrastructure.repos.company_repo import CompanyRepo
from app.infrastructure.repos.media_repo import MediaRepo
from app.infrastructure.repos.community_repo import CommunityRepo
from app.presentation.schemas.companies import CompanyCreateIn, CompanyUpdateIn, CompanyOut
from app.presentation.schemas.content import SkillOut, ContentSphereOut
from app.infrastructure.repos.sql_models import SkillModel, SphereModel
from sqlalchemy import select
from app.presentation.schemas.communities import CommunityCreateIn, CommunityUpdateIn, CommunityOut
from app.usecases.companies import CompanyUseCase
from app.usecases.communities import CommunityUseCase
from app.infrastructure.repos.membership_repo import MembershipRepo
from app.infrastructure.repos.follow_repo import FollowRepo

router = APIRouter()


async def _skills_from_tag_ids(session: AsyncSession, tag_ids: list[str]) -> list[SkillOut]:
    if not tag_ids:
        return []
    res = await session.execute(select(SkillModel).where(SkillModel.id.in_(tag_ids)))
    skill_models = res.scalars().all()
    sphere_ids = list({m.sphere_id for m in skill_models})
    spheres_map = {}
    if sphere_ids:
        sp_res = await session.execute(select(SphereModel).where(SphereModel.id.in_(sphere_ids)))
        spheres_map = {sp.id: sp for sp in sp_res.scalars().all()}
    by_id = {m.id: m for m in skill_models}
    out: list[SkillOut] = []
    for sid in tag_ids:
        m = by_id.get(sid)
        if not m:
            continue
        sp = spheres_map.get(m.sphere_id)
        out.append(SkillOut(
            id=m.id,
            title=m.title,
            sphere_id=m.sphere_id,
            sphere=(ContentSphereOut(id=sp.id, title=sp.title, background_color=sp.background_color, text_color=sp.text_color) if sp else None),
        ))
    return out


@router.post("/companies", response_model=CompanyOut, dependencies=[Depends(role_required("admin"))])
async def admin_create_company(data: CompanyCreateIn, session: AsyncSession = Depends(get_session)):
    uc = CompanyUseCase(companies=CompanyRepo(session))
    c = await uc.create(name=data.name, description=data.description, tags=data.tags)
    return CompanyOut(id=c.id, name=c.name, description=c.description, skills=await _skills_from_tag_ids(session, c.tags or []))


@router.patch("/companies/{company_id}", response_model=CompanyOut, dependencies=[Depends(role_required("admin"))])
async def admin_update_company(company_id: str, data: CompanyUpdateIn, session: AsyncSession = Depends(get_session)):
    uc = CompanyUseCase(companies=CompanyRepo(session))
    payload = data.model_dump(exclude_unset=True)
    media_uids = payload.pop("media_uids", None)
    c = await uc.update(company_id, **payload)
    if not c:
        raise HTTPException(404, "Not found")
    if media_uids is not None:
        await MediaRepo(session).replace_for_company(company_id, media_uids)
    return CompanyOut(id=c.id, name=c.name, description=c.description, skills=await _skills_from_tag_ids(session, c.tags or []))


@router.post("/communities", response_model=CommunityOut, dependencies=[Depends(role_required("admin"))])
async def admin_create_community(data: CommunityCreateIn, session: AsyncSession = Depends(get_session)):
    uc = CommunityUseCase(communities=CommunityRepo(session), members=MembershipRepo(session), follows=FollowRepo(session))
    c = await uc.create(
        name=data.name,
        company_id=data.company_id,
        tags=data.tags,
        description=data.description,
        telegram_url=data.telegram_url,
        logo_media_id=data.logo_media_id,
    )
    return CommunityOut(
        id=c.id,
        company_id=c.company_id,
        name=c.name,
        description=c.description,
        telegram_url=c.telegram_url,
        tags=c.tags,
        is_archived=c.is_archived,
        logo_media_id=c.logo_media_id,
    )


@router.patch("/communities/{community_id}", response_model=CommunityOut, dependencies=[Depends(role_required("admin"))])
async def admin_update_community(community_id: str, data: CommunityUpdateIn, session: AsyncSession = Depends(get_session)):
    uc = CommunityUseCase(communities=CommunityRepo(session), members=MembershipRepo(session), follows=FollowRepo(session))
    c = await uc.update(community_id, **data.model_dump(exclude_unset=True))
    if not c:
        raise HTTPException(404, "Not found")
    return CommunityOut(
        id=c.id,
        company_id=c.company_id,
        name=c.name,
        description=c.description,
        telegram_url=c.telegram_url,
        tags=c.tags,
        is_archived=c.is_archived,
        logo_media_id=c.logo_media_id,
    )
