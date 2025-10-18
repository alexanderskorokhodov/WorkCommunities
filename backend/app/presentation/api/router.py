from fastapi import APIRouter

from . import auth_endpoints
from . import content_endpoints
from . import media_endpoints
from . import events_endpoints
from . import companies_endpoints
from . import communities_endpoints
from . import admin_endpoints
from . import profiles_endpoints
from . import reference_endpoints
from . import users_endpoints

api = APIRouter()
api.include_router(auth_endpoints.router, prefix="/auth", tags=["auth"])
api.include_router(media_endpoints.router, prefix="/media", tags=["media"])
api.include_router(content_endpoints.router, prefix="/content", tags=["content"])
api.include_router(events_endpoints.router, prefix="/events", tags=["events"])
api.include_router(companies_endpoints.router, prefix="/companies", tags=["companies"])
api.include_router(communities_endpoints.router, prefix="/communities", tags=["communities"])
api.include_router(admin_endpoints.router, prefix="/admin", tags=["admin"])
api.include_router(profiles_endpoints.router, prefix="/profiles", tags=["profiles"])
api.include_router(reference_endpoints.router, prefix="/reference", tags=["reference"])
api.include_router(users_endpoints.router, prefix="/users", tags=["users"])
# NOTE: Other endpoints can be wired similarly.
