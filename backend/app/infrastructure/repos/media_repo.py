from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import Media, MediaType
from app.domain.repositories import IMediaRepo
from .sql_models import MediaModel, PostMediaModel


class MediaRepo(IMediaRepo):
    def __init__(self, session: AsyncSession):
        self.s = session

    async def create(self, *, uid: str, kind: str, mime: str, ext: str | None, size: int, url: str) -> Media:
        m = MediaModel(id=uid, kind=kind, mime=mime, ext=ext, size=size, url=url)
        self.s.add(m)
        await self.s.flush()
        return Media(id=m.id, kind=MediaType(m.kind), mime=m.mime, ext=m.ext, size=m.size, url=m.url,
                     created_at=m.created_at)

    async def get(self, media_id: str) -> Optional[Media]:
        res = await self.s.execute(select(MediaModel).where(MediaModel.id == media_id))
        m = res.scalar_one_or_none()
        if not m: return None
        return Media(id=m.id, kind=MediaType(m.kind), mime=m.mime, ext=m.ext, size=m.size, url=m.url,
                     created_at=m.created_at)

    async def attach_to_post(self, post_id: str, media_ids: list[str]) -> None:
        # порядковые индексы по очереди
        for idx, mid in enumerate(media_ids):
            self.s.add(PostMediaModel(post_id=post_id, media_id=mid, order_index=idx))
        await self.s.flush()

    async def list_for_post(self, post_id: str) -> Sequence[Media]:
        # join вручную, чтобы вернуть Media
        stmt = (
            select(MediaModel)
            .join(PostMediaModel, PostMediaModel.media_id == MediaModel.id)
            .where(PostMediaModel.post_id == post_id)
            .order_by(PostMediaModel.order_index.asc())
        )
        res = await self.s.execute(stmt)
        rows = res.scalars().all()
        return [
            Media(id=m.id, kind=MediaType(m.kind), mime=m.mime, ext=m.ext, size=m.size, url=m.url,
                  created_at=m.created_at)
            for m in rows
        ]
