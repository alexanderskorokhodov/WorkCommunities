from datetime import datetime
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import Story
from app.domain.repositories import IStoryRepo
from app.infrastructure.repos.sql_models import StoryModel


def _to_domain_story(m: StoryModel) -> Story:
    return Story(
        id=m.id,
        company_id=m.company_id,
        title=m.title,
        media_url=m.media_url,
        created_at=m.created_at,
    )


class StoryRepo(IStoryRepo):
    def __init__(self, s: AsyncSession):
        self.s = s

    async def create(self, company_id: str, title: str, media_url: str) -> Story:
        """Создать сторис (одно медиа)."""
        m = StoryModel(
            company_id=company_id,
            title=title,
            media_url=media_url,
            created_at=datetime.utcnow(),
        )
        self.s.add(m)
        await self.s.flush()
        return _to_domain_story(m)

    async def list(self, limit: int = 20) -> Sequence[Story]:
        res = await self.s.execute(
            select(StoryModel).order_by(StoryModel.created_at.desc()).limit(limit)
        )
        return [_to_domain_story(r) for r in res.scalars().all()]

    async def get(self, story_id: str) -> Story | None:
        res = await self.s.execute(select(StoryModel).where(StoryModel.id == story_id))
        row = res.scalar_one_or_none()
        return _to_domain_story(row) if row else None
