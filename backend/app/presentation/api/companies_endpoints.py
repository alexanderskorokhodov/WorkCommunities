from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.db import get_session
from app.core.deps import get_current_user
from app.infrastructure.repos.company_repo import CompanyRepo
from app.presentation.schemas.companies import CompanyOut
from app.usecases.companies import CompanyUseCase

router = APIRouter()


@router.get("/my", response_model=list[CompanyOut])
async def my_companies(session: AsyncSession = Depends(get_session), user=Depends(get_current_user)):
    uc = CompanyUseCase(companies=CompanyRepo(session))
    companies = await uc.get_companies_for_user(user.id)
    return [CompanyOut(id=c.id, name=c.name, description=c.description) for c in companies]

