from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import User
from app.domain.repositories import IUserRepo
from .sql_models import UserModel


class UserRepo(IUserRepo):
    def __init__(self, session: AsyncSession):
        self.s = session

    async def get_by_id(self, user_id: str):
        res = await self.s.execute(select(UserModel).where(UserModel.id == user_id))
        m = res.scalar_one_or_none()
        return None if not m else User(
            id=m.id,
            role=m.role,
            phone=m.phone,
            email=m.email,
            password_hash=m.password_hash,
            avatar_media_id=m.avatar_media_id,
            created_at=m.created_at,
        )

    async def get_by_phone(self, phone: str):
        res = await self.s.execute(select(UserModel).where(UserModel.phone == phone))
        m = res.scalar_one_or_none()
        return None if not m else User(
            id=m.id,
            role=m.role,
            phone=m.phone,
            email=m.email,
            password_hash=m.password_hash,
            avatar_media_id=m.avatar_media_id,
            created_at=m.created_at,
        )

    async def get_by_email(self, email: str):
        res = await self.s.execute(select(UserModel).where(UserModel.email == email))
        m = res.scalar_one_or_none()
        return None if not m else User(
            id=m.id,
            role=m.role,
            phone=m.phone,
            email=m.email,
            password_hash=m.password_hash,
            avatar_media_id=m.avatar_media_id,
            created_at=m.created_at,
        )

    async def create_student(self, phone: str) -> User:
        m = UserModel(role="student", phone=phone)
        self.s.add(m)
        await self.s.flush()
        return await self.get_by_id(m.id)

    async def create_company(self, email: str, password_hash: str, name: str) -> User:
        m = UserModel(role="company", email=email, password_hash=password_hash)
        self.s.add(m)
        await self.s.flush()
        return await self.get_by_id(m.id)

    async def list_all(self):
        res = await self.s.execute(select(UserModel).order_by(UserModel.created_at.desc()))
        rows = res.scalars().all()
        return [
            User(
                id=m.id,
                role=m.role,
                phone=m.phone,
                email=m.email,
                password_hash=m.password_hash,
                avatar_media_id=m.avatar_media_id,
                created_at=m.created_at,
            )
            for m in rows
        ]

    async def create_admin(self, email: str, password_hash: str) -> User:
        m = UserModel(role="admin", email=email, password_hash=password_hash)
        self.s.add(m)
        await self.s.flush()
        return await self.get_by_id(m.id)
