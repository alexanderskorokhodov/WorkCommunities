from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.db import get_session
from app.core.deps import get_current_user, role_required, get_current_company
from app.infrastructure.repos.company_repo import CompanyRepo
from app.infrastructure.repos.community_repo import CommunityRepo
from app.infrastructure.repos.company_follow_repo import CompanyFollowRepo
from app.infrastructure.repos.membership_repo import MembershipRepo
from app.infrastructure.repos.media_repo import MediaRepo
from app.presentation.schemas.companies import CompanyOut, CompanyUpdateIn, CompanyDetailOut
from app.presentation.schemas.content import MediaOut, SkillOut, ContentSphereOut
from app.infrastructure.repos.sql_models import SkillModel, SphereModel
from sqlalchemy import select
from app.presentation.schemas.communities import CommunityOut
from app.usecases.companies import CompanyUseCase

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


@router.get("/", response_model=list[CompanyOut])
async def list_companies(session: AsyncSession = Depends(get_session)):
    repo = CompanyRepo(session)
    companies = await repo.list_all()
    out: list[CompanyOut] = []
    for c in companies:
        skills = await _skills_from_tag_ids(session, c.tags)
        out.append(CompanyOut(id=c.id, name=c.name, description=c.description, logo_media_id=c.logo_media_id, skills=skills))
    return out


@router.get("/me", response_model=CompanyDetailOut, dependencies=[Depends(role_required("company"))])
async def get_my_company(session: AsyncSession = Depends(get_session), company=Depends(get_current_company)):
    # Build the same detailed payload as for GET /companies/{company_id}
    comm_repo = CommunityRepo(session)
    communities = await comm_repo.list_for_company(company.id)
    counts = await MembershipRepo(session).counts_for_communities([c.id for c in communities])
    media_repo = MediaRepo(session)
    media = await media_repo.list_for_company(company.id)

    return CompanyDetailOut(
        id=company.id,
        name=company.name,
        description=company.description,
        logo_media_id=company.logo_media_id,
        skills=await _skills_from_tag_ids(session, company.tags),
        media=[MediaOut(id=m.id, kind=m.kind.value if hasattr(m.kind, "value") else m.kind, mime=m.mime, ext=m.ext, size=m.size, url=m.url) for m in media],
        communities=[
            CommunityOut(
                id=i.id,
                company_id=i.company_id,
                name=i.name,
                description=i.description,
                telegram_url=i.telegram_url,
                tags=i.tags,
                is_archived=i.is_archived,
                logo_media_id=i.logo_media_id,
                members_count=counts.get(i.id, 0),
            )
            for i in communities
        ],
    )


@router.get("/{company_id}", response_model=CompanyDetailOut)
async def get_company(company_id: str, session: AsyncSession = Depends(get_session)):
    c_repo = CompanyRepo(session)
    company = await c_repo.get(company_id)
    if not company:
        raise HTTPException(404, "Not found")

    comm_repo = CommunityRepo(session)
    communities = await comm_repo.list_for_company(company_id)
    counts = await MembershipRepo(session).counts_for_communities([c.id for c in communities])
    media_repo = MediaRepo(session)
    media = await media_repo.list_for_company(company_id)

    return CompanyDetailOut(
        id=company.id,
        name=company.name,
        description=company.description,
        logo_media_id=company.logo_media_id,
        skills=await _skills_from_tag_ids(session, company.tags),
        media=[MediaOut(id=m.id, kind=m.kind.value if hasattr(m.kind, "value") else m.kind, mime=m.mime, ext=m.ext, size=m.size, url=m.url) for m in media],
        communities=[
            CommunityOut(
                id=i.id,
                company_id=i.company_id,
                name=i.name,
                description=i.description,
                telegram_url=i.telegram_url,
                tags=i.tags,
                is_archived=i.is_archived,
                logo_media_id=i.logo_media_id,
                members_count=counts.get(i.id, 0),
            )
            for i in communities
        ],
    )



@router.get("/me/followed", response_model=list[CompanyOut])
async def my_followed_companies(session: AsyncSession = Depends(get_session), user=Depends(get_current_user)):
    uc = CompanyUseCase(companies=CompanyRepo(session), company_follows=CompanyFollowRepo(session))
    companies = await uc.list_followed(user.id)
    out: list[CompanyOut] = []
    for c in companies:
        skills = await _skills_from_tag_ids(session, c.tags)
        out.append(CompanyOut(id=c.id, name=c.name, description=c.description, logo_media_id=c.logo_media_id, skills=skills))
    return out


@router.post("/{company_id}/follow")
async def follow_company(company_id: str, session: AsyncSession = Depends(get_session), user=Depends(get_current_user)):
    uc = CompanyUseCase(companies=CompanyRepo(session), company_follows=CompanyFollowRepo(session))
    await uc.follow(user.id, company_id)
    return {"status": "ok"}


@router.delete("/{company_id}/follow")
async def unfollow_company(company_id: str, session: AsyncSession = Depends(get_session), user=Depends(get_current_user)):
    uc = CompanyUseCase(companies=CompanyRepo(session), company_follows=CompanyFollowRepo(session))
    await uc.unfollow(user.id, company_id)
    return {"status": "ok"}


@router.patch("/me", response_model=CompanyOut)
async def update_my_company(
    data: CompanyUpdateIn,
    session: AsyncSession = Depends(get_session),
    company=Depends(get_current_company),
):
    payload = data.model_dump(exclude_unset=True)
    media_uids = payload.pop("media_uids", None)
    uc = CompanyUseCase(companies=CompanyRepo(session))
    c = await uc.update(company.id, **payload)
    if media_uids is not None:
        await MediaRepo(session).replace_for_company(company.id, media_uids)
    skills = await _skills_from_tag_ids(session, c.tags)
    return CompanyOut(id=c.id, name=c.name, description=c.description, logo_media_id=c.logo_media_id, skills=skills)
