from typing import Optional, Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import Community
from app.domain.repositories import ICommunityRepo
from .sql_models import CommunityModel, MembershipModel


def _from_row(m: CommunityModel) -> Community:
    return Community(
        id=m.id,
        company_id=m.company_id,
        name=m.name,
        description=m.description,
        telegram_url=m.telegram_url,
        tags=(m.tags.split(",") if m.tags else []),
        is_archived=m.is_archived,
    )


class CommunityRepo(ICommunityRepo):
    def __init__(self, s: AsyncSession):
        self.s = s

    async def create(self, **data) -> Community:
        tags = data.pop("tags", []) or []
        m = CommunityModel(**data, tags=",".join(tags) if tags else None)
        self.s.add(m)
        await self.s.flush()
        return _from_row(m)

    async def update(self, community_id: str, **data) -> Community:
        if "tags" in data and data["tags"] is not None:
            data["tags"] = ",".join(data["tags"]) if data["tags"] else None
        await self.s.execute(update(CommunityModel).where(CommunityModel.id == community_id).values(**data))
        res = await self.s.execute(select(CommunityModel).where(CommunityModel.id == community_id))
        row = res.scalar_one_or_none()
        return _from_row(row) if row else None

    async def archive(self, community_id: str) -> Community:
        await self.s.execute(update(CommunityModel).where(CommunityModel.id == community_id).values(is_archived=True))
        res = await self.s.execute(select(CommunityModel).where(CommunityModel.id == community_id))
        row = res.scalar_one_or_none()
        return _from_row(row) if row else None

    async def get(self, community_id: str) -> Optional[Community]:
        res = await self.s.execute(select(CommunityModel).where(CommunityModel.id == community_id))
        row = res.scalar_one_or_none()
        return _from_row(row) if row else None

    async def list_for_user(self, user_id: str) -> Sequence[Community]:
        stmt = (
            select(CommunityModel)
            .join(MembershipModel, MembershipModel.community_id == CommunityModel.id)
            .where(MembershipModel.user_id == user_id, CommunityModel.is_archived == False)
        )
        res = await self.s.execute(stmt)
        return [_from_row(r) for r in res.scalars().all()]

    async def list_for_company(self, company_id: str) -> Sequence[Community]:
        res = await self.s.execute(
            select(CommunityModel).where(CommunityModel.company_id == company_id, CommunityModel.is_archived == False)
        )
        return [_from_row(r) for r in res.scalars().all()]
