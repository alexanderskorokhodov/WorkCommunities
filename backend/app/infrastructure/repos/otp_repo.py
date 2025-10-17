
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.repositories import IOTPRepo
from .sql_models import OTPModel

class OTPRepo(IOTPRepo):
    def __init__(self, session: AsyncSession):
        self.s = session

    async def issue(self, phone: str, code: str, ttl_seconds: int):
        m = OTPModel(phone=phone, code=code, expires_at=datetime.utcnow() + timedelta(seconds=ttl_seconds))
        self.s.add(m)
        await self.s.flush()
        return m

    async def verify(self, phone: str, code: str) -> bool:
        res = await self.s.execute(
            select(OTPModel).where(OTPModel.phone == phone, OTPModel.code == code, OTPModel.consumed == False)
        )
        row = res.scalar_one_or_none()
        if not row or row.expires_at < datetime.utcnow():
            return False
        row.consumed = True
        await self.s.flush()
        return True
