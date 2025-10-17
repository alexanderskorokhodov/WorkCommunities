from app.domain.repositories import IPostRepo, IStoryRepo


class ContentUseCase:
    def __init__(self, posts: IPostRepo, stories: IStoryRepo):
        self.posts = posts
        self.stories = stories

    async def create_post(self, **data):
        return await self.posts.create(**data)

    async def update_post(self, post_id: str, **data):
        return await self.posts.update(post_id, **data)

    async def get_post(self, post_id: str):
        return await self.posts.get(post_id)

    async def featured_posts(self, limit: int = 20):
        return await self.posts.list_featured(limit)

    async def search_posts(self, query: str, limit: int = 20):
        return await self.posts.search(query, limit)

    async def create_story(self, **data):
        return await self.stories.create(**data)

    async def list_stories(self, limit: int = 20):
        return await self.stories.list(limit)

    async def get_story(self, story_id: str):
        return await self.stories.get(story_id)
