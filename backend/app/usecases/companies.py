from app.domain.repositories import ICompanyRepo, ICompanyFollowRepo


class CompanyUseCase:
    def __init__(self, companies: ICompanyRepo, company_follows: ICompanyFollowRepo | None = None):
        self.companies = companies
        self.company_follows = company_follows

    async def create(self, *, name: str, description: str | None = None, tags: list[str] | None = None):
        return await self.companies.create(name=name, description=description, tags=tags)

    async def update(self, company_id: str, **data):
        return await self.companies.update(company_id, **data)

    async def get_companies_for_user(self, user_id: str):
        return await self.companies.get_companies_for_user(user_id)

    async def follow(self, user_id: str, company_id: str):
        if not self.company_follows:
            raise RuntimeError("Company follow repo is not configured")
        return await self.company_follows.follow(user_id, company_id)

    async def unfollow(self, user_id: str, company_id: str):
        if not self.company_follows:
            raise RuntimeError("Company follow repo is not configured")
        return await self.company_follows.unfollow(user_id, company_id)

    async def list_followed(self, user_id: str):
        if not self.company_follows:
            return []
        return await self.company_follows.list_companies_for_user(user_id)
