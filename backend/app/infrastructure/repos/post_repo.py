from datetime import datetime
from typing import Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import Post
from app.domain.repositories import IPostRepo
from app.infrastructure.repos.sql_models import PostModel, PostMediaModel, FollowModel


def _to_domain_post(m: PostModel) -> Post:
    return Post(
        id=m.id,
        community_id=m.community_id,
        author_user_id=m.author_user_id,
        title=m.title,
        body=m.body,
        featured=m.featured,
        created_at=m.created_at,
    )


class PostRepo(IPostRepo):
    def __init__(self, s: AsyncSession):
        self.s = s

    async def create(
            self,
            author_user_id: str,
            community_id: str,
            title: str,
            body: str,
            media_ids: list[str] | None = None,
            featured: bool = False,
    ) -> Post:
        """Создать пост и прикрепить медиа."""
        m = PostModel(
            author_user_id=author_user_id,
            community_id=community_id,
            title=title,
            body=body,
            featured=featured,
            created_at=datetime.utcnow(),
        )
        self.s.add(m)
        await self.s.flush()

        if media_ids:
            for i, media_id in enumerate(media_ids):
                self.s.add(PostMediaModel(post_id=m.id, media_id=media_id, order_index=i))
            await self.s.flush()

        return _to_domain_post(m)

    async def update(self, post_id: str, **kwargs) -> Post | None:
        await self.s.execute(update(PostModel).where(PostModel.id == post_id).values(**kwargs))
        res = await self.s.execute(select(PostModel).where(PostModel.id == post_id))
        row = res.scalar_one_or_none()
        return _to_domain_post(row) if row else None

    async def get(self, post_id: str) -> Post | None:
        res = await self.s.execute(select(PostModel).where(PostModel.id == post_id))
        row = res.scalar_one_or_none()
        return _to_domain_post(row) if row else None

    async def list_featured(self, limit: int = 20) -> Sequence[Post]:
        res = await self.s.execute(
            select(PostModel).where(PostModel.featured == True)
            .order_by(PostModel.created_at.desc())
            .limit(limit)
        )
        return [_to_domain_post(r) for r in res.scalars().all()]

    async def list_featured_for_user(self, user_id: str, limit: int = 20) -> Sequence[Post]:
        res = await self.s.execute(
            select(PostModel)
            .where(PostModel.featured == True, PostModel.author_user_id == user_id)
            .order_by(PostModel.created_at.desc())
            .limit(limit)
        )
        return [_to_domain_post(r) for r in res.scalars().all()]

    async def search(self, query: str, limit: int = 20) -> Sequence[Post]:
        q = f"%{query.lower()}%"
        res = await self.s.execute(
            select(PostModel).where(PostModel.title.ilike(q) | PostModel.body.ilike(q)).limit(limit)
        )
        return [_to_domain_post(r) for r in res.scalars().all()]

    async def list_for_followed_communities(self, user_id: str, limit: int = 20) -> Sequence[Post]:
        res = await self.s.execute(
            select(PostModel)
            .join(FollowModel, FollowModel.community_id == PostModel.community_id)
            .where(FollowModel.user_id == user_id)
            .order_by(PostModel.created_at.desc())
            .limit(limit)
        )
        return [_to_domain_post(r) for r in res.scalars().all()]

    async def list_for_communities(self, community_ids: Sequence[str], limit: int = 20) -> Sequence[Post]:
        if not community_ids:
            return []
        res = await self.s.execute(
            select(PostModel)
            .where(PostModel.community_id.in_(community_ids))
            .order_by(PostModel.created_at.desc())
            .limit(limit)
        )
        return [_to_domain_post(r) for r in res.scalars().all()]
