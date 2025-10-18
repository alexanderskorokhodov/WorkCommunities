from typing import Sequence

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import CompanyFollow, Company
from app.domain.repositories import ICompanyFollowRepo
from .sql_models import CompanyFollowModel, CompanyModel


def _from_row(m: CompanyFollowModel) -> CompanyFollow:
    return CompanyFollow(id=m.id, user_id=m.user_id, company_id=m.company_id)


class CompanyFollowRepo(ICompanyFollowRepo):
    def __init__(self, s: AsyncSession):
        self.s = s

    async def follow(self, user_id: str, company_id: str) -> CompanyFollow:
        m = CompanyFollowModel(user_id=user_id, company_id=company_id)
        self.s.add(m)
        await self.s.flush()
        return _from_row(m)

    async def unfollow(self, user_id: str, company_id: str) -> None:
        await self.s.execute(
            delete(CompanyFollowModel).where(
                CompanyFollowModel.user_id == user_id,
                CompanyFollowModel.company_id == company_id,
            )
        )

    async def list_company_ids_for_user(self, user_id: str) -> Sequence[str]:
        res = await self.s.execute(
            select(CompanyFollowModel.company_id).where(CompanyFollowModel.user_id == user_id)
        )
        return [r for r, in res.all()]

    async def list_companies_for_user(self, user_id: str) -> Sequence[Company]:
        stmt = (
            select(CompanyModel)
            .join(CompanyFollowModel, CompanyFollowModel.company_id == CompanyModel.id)
            .where(CompanyFollowModel.user_id == user_id)
        )
        res = await self.s.execute(stmt)
        return [Company(id=r.id, name=r.name, description=r.description) for r in res.scalars().all()]

