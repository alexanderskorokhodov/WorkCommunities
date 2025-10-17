from fastapi import APIRouter

from . import auth_endpoints
from . import content_endpoints
from . import media_endpoints

api = APIRouter()
api.include_router(auth_endpoints.router, prefix="/auth", tags=["auth"])
api.include_router(media_endpoints.router, prefix="/media", tags=["media"])
api.include_router(content_endpoints.router, prefix="/content", tags=["content"])
# NOTE: Other endpoints can be wired similarly.
