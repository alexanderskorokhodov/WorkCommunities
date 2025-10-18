from datetime import datetime
from typing import Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import Post, Skill
from app.domain.repositories import IPostRepo
from app.infrastructure.repos.sql_models import ContentModel, ContentMediaModel, FollowModel, ContentSkillModel, SkillModel


def _parse_tags(tags: str | None) -> list[str]:
    if not tags:
        return []
    return [t.strip() for t in tags.split(",") if t.strip()]


def _to_domain_post(m: ContentModel) -> Post:
    return Post(
        id=m.id,
        community_id=m.community_id,
        title=m.title,
        body=m.body or "",
        created_at=m.created_at,
        tags=_parse_tags(m.tags),
        cost=m.cost,
        participant_payout=m.participant_payout,
    )


class PostRepo(IPostRepo):
    def __init__(self, s: AsyncSession):
        self.s = s

    async def create(
        self,
        community_id: str,
        title: str,
        body: str,
        media_ids: list[str] | None = None,
        tags: list[str] | None = None,
        skill_ids: list[str] | None = None,
        cost: int | None = None,
        participant_payout: int | None = None,
    ) -> Post:
        """Создать пост и прикрепить медиа."""
        m = ContentModel(
            community_id=community_id,
            type="post",
            title=title,
            body=body,
            created_at=datetime.utcnow(),
            tags=",".join(tags) if tags else None,
            cost=cost,
            participant_payout=participant_payout,
        )
        self.s.add(m)
        await self.s.flush()

        if media_ids:
            for i, media_id in enumerate(media_ids):
                self.s.add(ContentMediaModel(content_id=m.id, media_id=media_id, order_index=i))
            await self.s.flush()

        if skill_ids:
            for sid in skill_ids:
                self.s.add(ContentSkillModel(content_id=m.id, skill_id=sid))
            await self.s.flush()

        return _to_domain_post(m)

    async def update(self, post_id: str, **kwargs) -> Post | None:
        # transform known fields
        skill_ids = kwargs.pop("skill_ids", None)
        if "tags" in kwargs and isinstance(kwargs["tags"], list):
            kwargs["tags"] = ",".join(kwargs["tags"]) if kwargs["tags"] else None
        await self.s.execute(update(ContentModel).where(ContentModel.id == post_id).values(**kwargs))
        if skill_ids is not None:
            # reset mapping: simple strategy
            from sqlalchemy import delete
            await self.s.execute(delete(ContentSkillModel).where(ContentSkillModel.content_id == post_id))
            for sid in skill_ids:
                self.s.add(ContentSkillModel(content_id=post_id, skill_id=sid))
            await self.s.flush()
        res = await self.s.execute(select(ContentModel).where(ContentModel.id == post_id))
        row = res.scalar_one_or_none()
        return _to_domain_post(row) if row else None

    async def get(self, post_id: str) -> Post | None:
        res = await self.s.execute(select(ContentModel).where(ContentModel.id == post_id))
        row = res.scalar_one_or_none()
        return _to_domain_post(row) if row else None

    async def list_featured(self, limit: int = 20) -> Sequence[Post]:
        # Without 'featured' flag, return latest posts as a fallback
        res = await self.s.execute(
            select(ContentModel)
            .where(ContentModel.type == "post")
            .order_by(ContentModel.created_at.desc())
            .limit(limit)
        )
        return [_to_domain_post(r) for r in res.scalars().all()]

    async def list_featured_for_user(self, user_id: str, limit: int = 20) -> Sequence[Post]:
        # Fallback: posts from communities the user follows
        res = await self.s.execute(
            select(ContentModel)
            .join(FollowModel, FollowModel.community_id == ContentModel.community_id)
            .where(FollowModel.user_id == user_id, ContentModel.type == "post")
            .order_by(ContentModel.created_at.desc())
            .limit(limit)
        )
        return [_to_domain_post(r) for r in res.scalars().all()]

    async def list_latest_for_user(self, user_id: str, limit: int = 20) -> Sequence[Post]:
        # Without author linkage, reuse followed communities
        res = await self.s.execute(
            select(ContentModel)
            .join(FollowModel, FollowModel.community_id == ContentModel.community_id)
            .where(FollowModel.user_id == user_id, ContentModel.type == "post")
            .order_by(ContentModel.created_at.desc())
            .limit(limit)
        )
        return [_to_domain_post(r) for r in res.scalars().all()]

    async def search(self, query: str, limit: int = 20) -> Sequence[Post]:
        q = f"%{query.lower()}%"
        res = await self.s.execute(
            select(ContentModel)
            .where(ContentModel.type == "post")
            .where(ContentModel.title.ilike(q) | (ContentModel.body.ilike(q)))
            .limit(limit)
        )
        return [_to_domain_post(r) for r in res.scalars().all()]

    async def list_for_followed_communities(self, user_id: str, limit: int = 20) -> Sequence[Post]:
        res = await self.s.execute(
            select(ContentModel)
            .join(FollowModel, FollowModel.community_id == ContentModel.community_id)
            .where(FollowModel.user_id == user_id, ContentModel.type == "post")
            .order_by(ContentModel.created_at.desc())
            .limit(limit)
        )
        return [_to_domain_post(r) for r in res.scalars().all()]

    async def list_for_communities(self, community_ids: Sequence[str], limit: int = 20) -> Sequence[Post]:
        if not community_ids:
            return []
        res = await self.s.execute(
            select(ContentModel)
            .where(ContentModel.community_id.in_(community_ids), ContentModel.type == "post")
            .order_by(ContentModel.created_at.desc())
            .limit(limit)
        )
        return [_to_domain_post(r) for r in res.scalars().all()]

    async def list_for_community(self, community_id: str, *, offset: int = 0, limit: int = 20) -> Sequence[Post]:
        res = await self.s.execute(
            select(ContentModel)
            .where(ContentModel.community_id == community_id, ContentModel.type == "post")
            .order_by(ContentModel.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return [_to_domain_post(r) for r in res.scalars().all()]

    async def list_all(self, *, offset: int = 0, limit: int = 20) -> Sequence[Post]:
        res = await self.s.execute(
            select(ContentModel)
            .where(ContentModel.type == "post")
            .order_by(ContentModel.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return [_to_domain_post(r) for r in res.scalars().all()]

    async def list_skills_for_post(self, post_id: str) -> list[Skill]:
        stmt = (
            select(SkillModel)
            .join(ContentSkillModel, ContentSkillModel.skill_id == SkillModel.id)
            .where(ContentSkillModel.content_id == post_id)
        )
        res = await self.s.execute(stmt)
        skills = res.scalars().all()
        return [Skill(id=s.id, title=s.title, sphere_id=s.sphere_id) for s in skills]
