from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.db import get_session
from app.core.deps import get_current_user
from app.infrastructure.repos.community_repo import CommunityRepo
from app.infrastructure.repos.follow_repo import FollowRepo
from app.presentation.schemas.communities import CommunityOut
from app.usecases.communities import CommunityUseCase

router = APIRouter()


@router.get("/by-company/{company_id}", response_model=list[CommunityOut])
async def list_company_communities(company_id: str, session: AsyncSession = Depends(get_session)):
    repo = CommunityRepo(session)
    items = await repo.list_for_company(company_id)
    return [CommunityOut(id=i.id, company_id=i.company_id, name=i.name, tags=i.tags, is_archived=i.is_archived) for i in items]


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
