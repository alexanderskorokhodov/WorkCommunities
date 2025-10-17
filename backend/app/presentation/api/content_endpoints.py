from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.db import get_session
from app.core.deps import get_current_user
from app.infrastructure.repos.media_repo import MediaRepo
from app.infrastructure.repos.post_repo import PostRepo  # реализуй как прежде
from app.infrastructure.repos.story_repo import StoryRepo  # реализуй как прежде
from app.presentation.schemas.content import PostCreateIn, PostUpdateIn, PostOut, StoryCreateIn, StoryOut, MediaOut
from app.usecases.content import ContentUseCase

router = APIRouter()


def _media_to_out(m) -> MediaOut:
    return MediaOut(id=m.id, kind=m.kind.value if hasattr(m.kind, "value") else m.kind, mime=m.mime, ext=m.ext,
                    size=m.size, url=m.url)


@router.post("/posts", response_model=PostOut)
async def create_post(data: PostCreateIn, session: AsyncSession = Depends(get_session), user=Depends(get_current_user)):
    uc = ContentUseCase(posts=PostRepo(session), stories=StoryRepo(session), media=MediaRepo(session))
    post = await uc.create_post(
        author_user_id=user.id,
        community_id=data.community_id,
        title=data.title,
        body=data.body,
        featured=data.featured,
        media_uids=data.media_uids or [],
    )
    # собрать media
    media = await MediaRepo(session).list_for_post(post.id)
    return PostOut(
        id=post.id, community_id=post.community_id, author_user_id=post.author_user_id,
        title=post.title, body=post.body, featured=post.featured,
        media=[_media_to_out(m) for m in media]
    )


@router.patch("/posts/{post_id}", response_model=PostOut)
async def update_post(post_id: str, data: PostUpdateIn, session: AsyncSession = Depends(get_session),
                      user=Depends(get_current_user)):
    uc = ContentUseCase(posts=PostRepo(session), stories=StoryRepo(session), media=MediaRepo(session))
    post = await uc.update_post(post_id, **data.model_dump(exclude_unset=True))
    media = await MediaRepo(session).list_for_post(post.id)
    return PostOut(
        id=post.id, community_id=post.community_id, author_user_id=post.author_user_id,
        title=post.title, body=post.body, featured=post.featured,
        media=[_media_to_out(m) for m in media]
    )


@router.get("/posts/{post_id}", response_model=PostOut)
async def get_post(post_id: str, session: AsyncSession = Depends(get_session)):
    uc = ContentUseCase(posts=PostRepo(session), stories=StoryRepo(session), media=MediaRepo(session))
    post, media = await uc.get_post_full(post_id)
    if not post:
        raise HTTPException(404, "Not found")
    return PostOut(
        id=post.id, community_id=post.community_id, author_user_id=post.author_user_id,
        title=post.title, body=post.body, featured=post.featured,
        media=[_media_to_out(m) for m in media]
    )


@router.post("/stories", response_model=StoryOut)
async def create_story(data: StoryCreateIn, session: AsyncSession = Depends(get_session),
                       user=Depends(get_current_user)):
    uc = ContentUseCase(posts=PostRepo(session), stories=StoryRepo(session), media=MediaRepo(session))
    try:
        story = await uc.create_story(company_id=data.company_id, title=data.title, media_uid=data.media_uid)
    except ValueError:
        raise HTTPException(400, "Media not found")
    m = await MediaRepo(session).get(story.media_id) if getattr(story, "media_id", None) else None
    return StoryOut(id=story.id, community_id=story.community_id, title=story.title, media_url=story.media_url,
                    media=_media_to_out(m) if m else None)


@router.get("/stories/{story_id}", response_model=StoryOut)
async def get_story(story_id: str, session: AsyncSession = Depends(get_session)):
    uc = ContentUseCase(posts=PostRepo(session), stories=StoryRepo(session), media=MediaRepo(session))
    story, m = await uc.get_story_full(story_id)
    if not story:
        raise HTTPException(404, "Not found")
    return StoryOut(id=story.id, community_id=story.community_id, title=story.title, media_url=story.media_url,
                    media=_media_to_out(m) if m else None)
