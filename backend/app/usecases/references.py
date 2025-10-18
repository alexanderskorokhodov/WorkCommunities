from typing import Optional

from app.domain.entities import Sphere, Skill, Status
from app.infrastructure.repos.reference_repo import ReferenceRepo


class ReferenceUseCase:
    def __init__(self, refs: ReferenceRepo):
        self.refs = refs

    async def list_spheres(self) -> list[Sphere]:
        return list(await self.refs.list_spheres())

    async def list_skills(self, *, sphere_id: Optional[str] = None) -> list[Skill]:
        return list(await self.refs.list_skills(sphere_id=sphere_id))

    async def list_statuses(self) -> list[Status]:
        return list(await self.refs.list_statuses())

