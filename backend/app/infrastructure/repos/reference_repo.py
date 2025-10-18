from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import Sphere, Skill, Status
from .sql_models import SphereModel, SkillModel, StatusModel


def _sphere_from_row(m: SphereModel) -> Sphere:
    return Sphere(id=m.id, title=m.title, background_color=m.background_color, text_color=m.text_color)


def _skill_from_row(m: SkillModel, sphere: Optional[Sphere] = None) -> Skill:
    return Skill(id=m.id, title=m.title, sphere_id=m.sphere_id, sphere=sphere)


def _status_from_row(m: StatusModel) -> Status:
    return Status(id=m.id, title=m.title)


class ReferenceRepo:
    def __init__(self, s: AsyncSession):
        self.s = s

    async def list_spheres(self) -> Sequence[Sphere]:
        res = await self.s.execute(select(SphereModel))
        return [_sphere_from_row(m) for m in res.scalars().all()]

    async def list_skills(self, *, sphere_id: Optional[str] = None) -> Sequence[Skill]:
        query = select(SkillModel)
        if sphere_id:
            query = query.where(SkillModel.sphere_id == sphere_id)
        res = await self.s.execute(query)
        skill_models = res.scalars().all()
        # preload spheres
        sphere_ids = list({m.sphere_id for m in skill_models})
        spheres_map: dict[str, Sphere] = {}
        if sphere_ids:
            sp_res = await self.s.execute(select(SphereModel).where(SphereModel.id.in_(sphere_ids)))
            spheres_map = {sp.id: _sphere_from_row(sp) for sp in sp_res.scalars().all()}
        return [_skill_from_row(m, spheres_map.get(m.sphere_id)) for m in skill_models]

    async def list_statuses(self) -> Sequence[Status]:
        res = await self.s.execute(select(StatusModel))
        return [_status_from_row(m) for m in res.scalars().all()]

