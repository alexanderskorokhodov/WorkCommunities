from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.db import get_session
from app.infrastructure.repos.user_repo import UserRepo
from app.presentation.schemas.users import UserOut


router = APIRouter()


@router.get("/", response_model=list[UserOut])
async def list_users(session: AsyncSession = Depends(get_session)):
    repo = UserRepo(session)
    users = await repo.list_all()
    return [
        UserOut(
            id=u.id,
            role=u.role,
            phone=u.phone,
            email=u.email,
            created_at=u.created_at,
        )
        for u in users
    ]

