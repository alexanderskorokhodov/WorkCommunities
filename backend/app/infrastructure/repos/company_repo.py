from typing import Optional, Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import Company
from app.domain.repositories import ICompanyRepo
from .sql_models import CompanyModel, CommunityModel, MembershipModel


def _from_row(m: CompanyModel) -> Company:
    return Company(id=m.id, name=m.name, description=m.description, logo_media_id=m.logo_media_id)


class CompanyRepo(ICompanyRepo):
    def __init__(self, s: AsyncSession):
        self.s = s

    async def get(self, company_id: str) -> Optional[Company]:
        res = await self.s.execute(select(CompanyModel).where(CompanyModel.id == company_id))
        row = res.scalar_one_or_none()
        return _from_row(row) if row else None

    async def create(self, *, name: str, description: str | None = None, owner_user_id: str | None = None) -> Company:
        m = CompanyModel(name=name, description=description, owner_user_id=owner_user_id)
        self.s.add(m)
        await self.s.flush()
        return _from_row(m)

    async def update(self, company_id: str, **data) -> Company:
        await self.s.execute(update(CompanyModel).where(CompanyModel.id == company_id).values(**data))
        res = await self.s.execute(select(CompanyModel).where(CompanyModel.id == company_id))
        row = res.scalar_one_or_none()
        return _from_row(row) if row else None

    async def get_companies_for_user(self, user_id: str) -> Sequence[Company]:
        stmt = (
            select(CompanyModel).distinct()
            .join(CommunityModel, CommunityModel.company_id == CompanyModel.id)
            .join(MembershipModel, MembershipModel.community_id == CommunityModel.id)
            .where(MembershipModel.user_id == user_id)
        )
        res = await self.s.execute(stmt)
        return [_from_row(r) for r in res.scalars().all()]

    async def list_all(self) -> Sequence[Company]:
        res = await self.s.execute(select(CompanyModel))
        return [_from_row(r) for r in res.scalars().all()]

    async def get_by_owner(self, user_id: str) -> Optional[Company]:
        res = await self.s.execute(select(CompanyModel).where(CompanyModel.owner_user_id == user_id))
        row = res.scalar_one_or_none()
        return _from_row(row) if row else None
