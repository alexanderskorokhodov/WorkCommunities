from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.db import get_session
from app.core.deps import get_current_user, role_required
from app.infrastructure.repos.community_repo import CommunityRepo
from app.infrastructure.repos.follow_repo import FollowRepo
from app.presentation.schemas.communities import CommunityOut, CommunityCreateIn, CommunityUpdateIn
from app.usecases.communities import CommunityUseCase

router = APIRouter()


@router.get("/by-company/{company_id}", response_model=list[CommunityOut])
async def list_company_communities(company_id: str, session: AsyncSession = Depends(get_session)):
    repo = CommunityRepo(session)
    items = await repo.list_for_company(company_id)
    return [
        CommunityOut(
            id=i.id,
            company_id=i.company_id,
            name=i.name,
            description=i.description,
            telegram_url=i.telegram_url,
            tags=i.tags,
            is_archived=i.is_archived,
        )
        for i in items
    ]


@router.post("/", response_model=CommunityOut, dependencies=[Depends(role_required("company"))])
async def create_community(data: CommunityCreateIn, session: AsyncSession = Depends(get_session)):
    # Note: until user->company mapping exists, require explicit company_id
    if not data.company_id:
        raise HTTPException(400, "company_id is required")
    uc = CommunityUseCase(communities=CommunityRepo(session), members=None, follows=FollowRepo(session))
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


@router.patch("/{community_id}", response_model=CommunityOut, dependencies=[Depends(role_required("company"))])
async def update_community(community_id: str, data: CommunityUpdateIn, session: AsyncSession = Depends(get_session)):
    uc = CommunityUseCase(communities=CommunityRepo(session), members=None, follows=FollowRepo(session))
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


@router.post("/{community_id}/follow")
async def follow_community(community_id: str, session: AsyncSession = Depends(get_session), user=Depends(get_current_user)):
    uc = CommunityUseCase(communities=CommunityRepo(session), members=None, follows=FollowRepo(session))
    await uc.follow(user.id, community_id)
    return {"status": "ok"}


@router.delete("/{community_id}/follow")
async def unfollow_community(community_id: str, session: AsyncSession = Depends(get_session), user=Depends(get_current_user)):
    uc = CommunityUseCase(communities=CommunityRepo(session), members=None, follows=FollowRepo(session))
    await uc.unfollow(user.id, community_id)
    return {"status": "ok"}
