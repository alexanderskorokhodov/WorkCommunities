import mimetypes
import os

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.db import get_session
from app.domain.entities import MediaType
from app.infrastructure.repos.media_repo import MediaRepo
from app.infrastructure.services.storage import LocalFileStorage

router = APIRouter()

storage = LocalFileStorage(root="/data/media", public_prefix="/media")


def _guess_kind(mime: str) -> str:
    if mime.startswith("image/"): return MediaType.image.value
    if mime.startswith("video/"): return MediaType.video.value
    return MediaType.other.value


@router.post("/upload")
async def upload_media(file: UploadFile = File(...), session: AsyncSession = Depends(get_session)):
    mime = file.content_type or mimetypes.guess_type(file.filename or "")[0] or "application/octet-stream"
    ext = os.path.splitext(file.filename or "")[1].lstrip(".").lower() or None
    uid, url = storage.save(file.file, mime=mime, ext=ext)
    size = file.spool_max_size or 0  # не всегда корректно — можно os.path.getsize(storage.path_for(uid))
    repo = MediaRepo(session)
    media = await repo.create(id=uid, kind=_guess_kind(mime), mime=mime, ext=ext, size=size, url=url)
    return {
        "id": media.id, "kind": media.kind.value, "mime": media.mime, "ext": media.ext, "size": media.size,
        "url": media.url
    }


@router.get("/{media_id}")
async def get_media(media_id: str):
    path = storage.path_for(media_id)
    if not os.path.exists(path):
        raise HTTPException(404, "Not found")
    return FileResponse(path)
