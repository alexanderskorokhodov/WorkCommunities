from app.domain.repositories import IPostRepo, IStoryRepo, IMediaRepo


class ContentUseCase:
    def __init__(self, posts: IPostRepo, stories: IStoryRepo, media: IMediaRepo):
        self.posts = posts
        self.stories = stories
        self.media = media

    async def create_post(self, *, author_user_id: str, community_id: str, title: str, body: str, featured: bool,
                          media_uids: list[str]):
        post = await self.posts.create(community_id=community_id, author_user_id=author_user_id, title=title, body=body,
                                       featured=featured)
        if media_uids:
            await self.media.attach_to_post(post.id, media_uids)
        return post

    async def update_post(self, post_id: str, **data):
        media_uids = data.pop("media_uids", None)
        post = await self.posts.update(post_id, **data)
        if media_uids is not None:
            # простая стратегия: удалить связи и записать заново (или сделать upsert)
            # тут можно реализовать repo.reset_post_media(...)
            await self.media.attach_to_post(post_id, media_uids)
        return post

    async def get_post_full(self, post_id: str):
        post = await self.posts.get(post_id)
        media = await self.media.list_for_post(post_id)
        return post, media

    async def create_story(self, *, community_id: str, title: str, media_uid: str):
        m = await self.media.get(media_uid)
        if not m: raise ValueError("Media not found")
        story = await self.stories.create(community_id=community_id, title=title, media_url=m.url, media_id=m.id)
        return story

    async def get_story_full(self, story_id: str):
        story = await self.stories.get(story_id)
        m = None
        if getattr(story, "media_id", None):
            m = await self.media.get(story.media_id)
        return story, m

    async def get_post(self, post_id: str):
        return await self.posts.get(post_id)

    async def featured_posts(self, limit: int = 20):
        return await self.posts.list_featured(limit)

    async def search_posts(self, query: str, limit: int = 20):
        return await self.posts.search(query, limit)

    async def list_stories(self, limit: int = 20):
        return await self.stories.list(limit)

    async def get_story(self, story_id: str):
        return await self.stories.get(story_id)
