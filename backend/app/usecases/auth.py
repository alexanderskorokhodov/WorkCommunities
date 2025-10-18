from app.core.config import settings
from app.core.security import create_access_token, hash_password, verify_password
from app.domain.repositories import IUserRepo, IOTPRepo, ICompanyRepo


class AuthUseCase:
    def __init__(self, users: IUserRepo, otps: IOTPRepo, companies: ICompanyRepo | None = None):
        self.users = users
        self.otps = otps
        self.companies = companies

    async def request_otp(self, phone: str) -> None:
        # code = f"{random.randint(10000, 99999)}"  # 5-digit code
        code = "11111"
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
        company_id = None
        if self.companies:
            c = await self.companies.create(name=name, owner_user_id=user.id)
            company_id = c.id
        return create_access_token(subject=user.id, role="company", company_id=company_id)

    async def company_login(self, email: str, password: str) -> str:
        user = await self.users.get_by_email(email)
        if not user or not user.password_hash or not verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")
        company_id = None
        if self.companies:
            c = await self.companies.get_by_owner(user.id)
            company_id = c.id if c else None
        return create_access_token(subject=user.id, role="company", company_id=company_id)

    async def admin_signup(self, email: str, password: str, signup_token: str | None) -> str:
        if not settings.ADMIN_SIGNUP_TOKEN or signup_token != settings.ADMIN_SIGNUP_TOKEN:
            raise PermissionError("Forbidden")
        if await self.users.get_by_email(email):
            raise ValueError("Email already registered")
        ph = hash_password(password)
        user = await self.users.create_admin(email, ph)
        return create_access_token(subject=user.id, role="admin")

    async def admin_login(self, email: str, password: str) -> str:
        user = await self.users.get_by_email(email)
        if not user or user.role != "admin" or not user.password_hash or not verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")
        return create_access_token(subject=user.id, role="admin")
