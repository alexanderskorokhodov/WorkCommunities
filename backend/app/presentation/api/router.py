from fastapi import APIRouter

from . import auth_endpoints

api = APIRouter()
api.include_router(auth_endpoints.router, prefix="/auth", tags=["auth"])

# NOTE: Other endpoints can be wired similarly.
