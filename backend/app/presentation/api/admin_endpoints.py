from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.db import get_session
from app.core.deps import role_required
from app.infrastructure.repos.company_repo import CompanyRepo
from app.infrastructure.repos.community_repo import CommunityRepo
from app.presentation.schemas.companies import CompanyCreateIn, CompanyUpdateIn, CompanyOut
from app.presentation.schemas.communities import CommunityCreateIn, CommunityUpdateIn, CommunityOut
from app.usecases.companies import CompanyUseCase
from app.usecases.communities import CommunityUseCase
from app.infrastructure.repos.membership_repo import MembershipRepo
from app.infrastructure.repos.follow_repo import FollowRepo

router = APIRouter()


@router.post("/companies", response_model=CompanyOut, dependencies=[Depends(role_required("company"))])
async def admin_create_company(data: CompanyCreateIn, session: AsyncSession = Depends(get_session)):
    uc = CompanyUseCase(companies=CompanyRepo(session))
    c = await uc.create(name=data.name, description=data.description)
    return CompanyOut(id=c.id, name=c.name, description=c.description)


@router.patch("/companies/{company_id}", response_model=CompanyOut, dependencies=[Depends(role_required("company"))])
async def admin_update_company(company_id: str, data: CompanyUpdateIn, session: AsyncSession = Depends(get_session)):
    uc = CompanyUseCase(companies=CompanyRepo(session))
    c = await uc.update(company_id, **data.model_dump(exclude_unset=True))
    if not c:
        raise HTTPException(404, "Not found")
    return CompanyOut(id=c.id, name=c.name, description=c.description)


@router.post("/communities", response_model=CommunityOut, dependencies=[Depends(role_required("company"))])
async def admin_create_community(data: CommunityCreateIn, session: AsyncSession = Depends(get_session)):
    uc = CommunityUseCase(communities=CommunityRepo(session), members=MembershipRepo(session), follows=FollowRepo(session))
    c = await uc.create(
        name=data.name,
        company_id=data.company_id,
        tags=data.tags,
        description=data.description,
        telegram_url=data.telegram_url,
    )
    return CommunityOut(
        id=c.id,
        company_id=c.company_id,
        name=c.name,
        description=c.description,
        telegram_url=c.telegram_url,
        tags=c.tags,
        is_archived=c.is_archived,
    )


@router.patch("/communities/{community_id}", response_model=CommunityOut, dependencies=[Depends(role_required("company"))])
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
    )
