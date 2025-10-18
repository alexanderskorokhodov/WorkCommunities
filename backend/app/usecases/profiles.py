from app.domain.repositories import IProfileRepo


class ProfileUseCase:
    def __init__(self, profiles: IProfileRepo):
        self.profiles = profiles

    async def create(self, user_id: str, **data):
        return await self.profiles.create(user_id, **data)

    async def get(self, profile_id: str):
        return await self.profiles.get(profile_id)

    async def update(self, user_id: str, **data):
        return await self.profiles.update(user_id, **data)

    async def get_or_create_for_user(self, user_id: str):
        return await self.profiles.get_or_create_for_user(user_id)
