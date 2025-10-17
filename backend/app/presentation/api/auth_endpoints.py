
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.adapters.db import get_session
from app.presentation.schemas.auth import PhoneIn, OTPVerifyIn, TokenOut, CompanySignupIn, CompanyLoginIn
from app.usecases.auth import AuthUseCase
from app.infrastructure.repos.user_repo import UserRepo
from app.infrastructure.repos.otp_repo import OTPRepo

router = APIRouter()

@router.post("/otp/request", status_code=204)
async def request_otp(data: PhoneIn, session: AsyncSession = Depends(get_session)):
    uc = AuthUseCase(users=UserRepo(session), otps=OTPRepo(session))
    await uc.request_otp(data.phone)
    return None

@router.post("/otp/verify", response_model=TokenOut)
async def verify_otp(data: OTPVerifyIn, session: AsyncSession = Depends(get_session)):
    uc = AuthUseCase(users=UserRepo(session), otps=OTPRepo(session))
    try:
        token = await uc.verify_otp(data.phone, data.code)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid code")
    return TokenOut(access_token=token)

@router.post("/company/signup", response_model=TokenOut)
async def company_signup(data: CompanySignupIn, session: AsyncSession = Depends(get_session)):
    uc = AuthUseCase(users=UserRepo(session), otps=OTPRepo(session))
    try:
        token = await uc.company_signup(data.email, data.password, data.name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return TokenOut(access_token=token)

@router.post("/company/login", response_model=TokenOut)
async def company_login(data: CompanyLoginIn, session: AsyncSession = Depends(get_session)):
    uc = AuthUseCase(users=UserRepo(session), otps=OTPRepo(session))
    try:
        token = await uc.company_login(data.email, data.password)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return TokenOut(access_token=token)
