import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.adapters.db import get_session
from app.core.config import settings
from app.infrastructure.repos.user_repo import UserRepo
from app.infrastructure.repos.company_repo import CompanyRepo

bearer = HTTPBearer(auto_error=False)


async def get_current_user(
        creds: HTTPAuthorizationCredentials | None = Depends(bearer),
        session=Depends(get_session),
):
    if not creds:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        payload = jwt.decode(creds.credentials, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
        uid: str = payload.get("sub")
        role: str = payload.get("role")
        if not uid:
            raise ValueError("Missing sub")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = await UserRepo(session).get_by_id(uid)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def role_required(*roles: str):
    async def _checker(user=Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user

    return _checker


async def get_current_company(
    user=Depends(role_required("company")),
    session=Depends(get_session),
    creds: HTTPAuthorizationCredentials | None = Depends(bearer),
):
    # First try owner linkage
    repo = CompanyRepo(session)
    company = await repo.get_by_owner(user.id)
    if company:
        return company
    # If token carries company_id, use it
    if creds:
        try:
            payload = jwt.decode(creds.credentials, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
            company_id: str | None = payload.get("company_id")
            if company_id:
                c2 = await repo.get(company_id)
                if c2:
                    return c2
        except Exception:
            pass
    raise HTTPException(status_code=403, detail="Company is not set for this user")
