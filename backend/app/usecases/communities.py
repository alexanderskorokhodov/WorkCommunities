
from app.domain.repositories import ICommunityRepo, IMembershipRepo, IFollowRepo

class CommunityUseCase:
    def __init__(self, communities: ICommunityRepo, members: IMembershipRepo, follows: IFollowRepo):
        self.communities = communities
        self.members = members
        self.follows = follows

    async def create(self, *, name: str, company_id: str | None, tags: list[str]):
        return await self.communities.create(name=name, company_id=company_id, tags=tags, is_archived=False)

    async def update(self, community_id: str, **data):
        return await self.communities.update(community_id, **data)

    async def archive(self, community_id: str):
        return await self.communities.archive(community_id)

    async def follow(self, user_id: str, community_id: str):
        return await self.follows.follow(user_id, community_id)

    async def unfollow(self, user_id: str, community_id: str):
        return await self.follows.unfollow(user_id, community_id)

    async def join(self, user_id: str, community_id: str):
        return await self.members.join(user_id, community_id)

    async def exit(self, user_id: str, community_id: str):
        return await self.members.exit(user_id, community_id)
