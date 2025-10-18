from typing import Optional, Sequence

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import Case
from .sql_models import CaseModel


def _from_row(m: CaseModel) -> Case:
    return Case(
        id=m.id,
        community_id=m.community_id,
        title=m.title,
        description=m.description,
        date=m.date,
        points=m.points,
    )


class CaseRepo:
    def __init__(self, s: AsyncSession):
        self.s = s

    async def create(self, **data) -> Case:
        m = CaseModel(**data)
        self.s.add(m)
        await self.s.flush()
        return _from_row(m)

    async def get_by_id(self, case_id: str) -> Optional[Case]:
        res = await self.s.execute(select(CaseModel).where(CaseModel.id == case_id))
        row = res.scalar_one_or_none()
        return _from_row(row) if row else None

    async def list_for_community(self, community_id: str) -> Sequence[Case]:
        res = await self.s.execute(select(CaseModel).where(CaseModel.community_id == community_id))
        return [_from_row(r) for r in res.scalars().all()]

    async def delete(self, case_id: str) -> None:
        await self.s.execute(delete(CaseModel).where(CaseModel.id == case_id))
