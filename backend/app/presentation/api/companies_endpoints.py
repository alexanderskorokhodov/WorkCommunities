from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.db import get_session
from app.core.deps import get_current_user, role_required, get_current_company
from app.infrastructure.repos.company_repo import CompanyRepo
from app.infrastructure.repos.community_repo import CommunityRepo
from app.infrastructure.repos.company_follow_repo import CompanyFollowRepo
from app.presentation.schemas.companies import CompanyOut, CompanyUpdateIn, CompanyDetailOut
from app.presentation.schemas.communities import CommunityOut
from app.usecases.companies import CompanyUseCase

router = APIRouter()


@router.get("/", response_model=list[CompanyOut])
async def list_companies(session: AsyncSession = Depends(get_session)):
    repo = CompanyRepo(session)
    companies = await repo.list_all()
    return [CompanyOut(id=c.id, name=c.name, description=c.description, logo_media_id=c.logo_media_id, tags=c.tags) for c in companies]


@router.get("/{company_id}", response_model=CompanyDetailOut)
async def get_company(company_id: str, session: AsyncSession = Depends(get_session)):
    c_repo = CompanyRepo(session)
    company = await c_repo.get(company_id)
    if not company:
        raise HTTPException(404, "Not found")

    comm_repo = CommunityRepo(session)
    communities = await comm_repo.list_for_company(company_id)

    return CompanyDetailOut(
        id=company.id,
        name=company.name,
        description=company.description,
        logo_media_id=company.logo_media_id,
        tags=company.tags,
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
            )
            for i in communities
        ],
    )


@router.get("/me/followed", response_model=list[CompanyOut])
async def my_followed_companies(session: AsyncSession = Depends(get_session), user=Depends(get_current_user)):
    uc = CompanyUseCase(companies=CompanyRepo(session), company_follows=CompanyFollowRepo(session))
    companies = await uc.list_followed(user.id)
    return [CompanyOut(id=c.id, name=c.name, description=c.description, logo_media_id=c.logo_media_id, tags=c.tags) for c in companies]


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
    uc = CompanyUseCase(companies=CompanyRepo(session))
    c = await uc.update(company.id, **data.model_dump(exclude_unset=True))
    return CompanyOut(id=c.id, name=c.name, description=c.description, logo_media_id=c.logo_media_id, tags=c.tags)
