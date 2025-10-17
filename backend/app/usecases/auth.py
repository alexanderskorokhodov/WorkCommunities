from app.core.config import settings
from app.core.security import create_access_token, hash_password, verify_password
from app.domain.repositories import IUserRepo, IOTPRepo


class AuthUseCase:
    def __init__(self, users: IUserRepo, otps: IOTPRepo):
        self.users = users
        self.otps = otps

    async def request_otp(self, phone: str) -> None:
        import random
        code = f"{random.randint(100000, 999999)}"
        await self.otps.issue(phone, code, settings.OTP_TTL_SECONDS)

    async def verify_otp(self, phone: str, code: str) -> str:
        ok = await self.otps.verify(phone, code)
        if not ok:
            raise ValueError("Invalid or expired code")
        user = await self.users.get_by_phone(phone)
        if not user:
            user = await self.users.create_student(phone)
        token = create_access_token(subject=user.id, role="student")
        return token

    async def company_signup(self, email: str, password: str, name: str) -> str:
        if await self.users.get_by_email(email):
            raise ValueError("Email already registered")
        ph = hash_password(password)
        user = await self.users.create_company(email, ph, name)
        return create_access_token(subject=user.id, role="company")

    async def company_login(self, email: str, password: str) -> str:
        user = await self.users.get_by_email(email)
        if not user or not user.password_hash or not verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")
        return create_access_token(subject=user.id, role="company")
