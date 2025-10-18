from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.db import get_session
from app.infrastructure.repos.community_repo import CommunityRepo
from app.presentation.schemas.communities import CommunityOut

router = APIRouter()


@router.get("/by-company/{company_id}", response_model=list[CommunityOut])
async def list_company_communities(company_id: str, session: AsyncSession = Depends(get_session)):
    repo = CommunityRepo(session)
    items = await repo.list_for_company(company_id)
    return [CommunityOut(id=i.id, company_id=i.company_id, name=i.name, tags=i.tags, is_archived=i.is_archived) for i in items]

