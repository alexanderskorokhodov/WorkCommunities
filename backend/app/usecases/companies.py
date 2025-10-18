from app.domain.repositories import ICompanyRepo


class CompanyUseCase:
    def __init__(self, companies: ICompanyRepo):
        self.companies = companies

    async def create(self, *, name: str, description: str | None = None):
        return await self.companies.create(name=name, description=description)

    async def update(self, company_id: str, **data):
        return await self.companies.update(company_id, **data)

    async def get_companies_for_user(self, user_id: str):
        return await self.companies.get_companies_for_user(user_id)

