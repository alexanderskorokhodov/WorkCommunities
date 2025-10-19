from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.adapters.db import get_session
from app.core.deps import get_current_user, role_required
from app.infrastructure.repos.media_repo import MediaRepo
from app.infrastructure.repos.post_repo import PostRepo  # реализуй как прежде
from app.infrastructure.repos.story_repo import StoryRepo  # реализуй как прежде
from app.infrastructure.repos.company_follow_repo import CompanyFollowRepo
from app.infrastructure.repos.sql_models import ContentModel
from app.presentation.schemas.content import PostCreateIn, PostUpdateIn, PostOut, StoryCreateIn, StoryOut, MediaOut, SkillOut, ContentItemOut, ContentSphereOut
from app.usecases.content import ContentUseCase

router = APIRouter()


def _media_to_out(m) -> MediaOut:
    return MediaOut(id=m.id, kind=m.kind.value if hasattr(m.kind, "value") else m.kind, mime=m.mime, ext=m.ext,
                    size=m.size, url=m.url)


@router.get("/posts", response_model=list[ContentItemOut])
async def list_posts(offset: int = 0, limit: int = 20, session: AsyncSession = Depends(get_session)):
    """Unified feed: posts + events, sorted by created_at desc."""
    media_repo = MediaRepo(session)
    stmt = (
        select(ContentModel)
        .order_by(ContentModel.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    res = await session.execute(stmt)
    items = res.scalars().all()
    result: list[ContentItemOut] = []
    for c in items:
        media = await media_repo.list_for_content(c.id)
        if not media and getattr(c, "media_id", None):
            m = await media_repo.get(c.media_id)
            if m:
                media = [m]
        body = c.body if c.type == "post" else (c.description or None)
        # tags parsing from comma-separated string
        tags = [t.strip() for t in (c.tags or "").split(",") if t.strip()]
        # skills via PostRepo utility (content_id works for both types)
        skills = await PostRepo(session).list_skills_for_post(c.id)
        def _skill_to_out(s) -> SkillOut:
            sp = getattr(s, "sphere", None)
            return SkillOut(
                id=s.id,
                title=s.title,
                sphere_id=s.sphere_id,
                sphere=(
                    ContentSphereOut(
                        id=sp.id,
                        title=sp.title,
                        background_color=sp.background_color,
                        text_color=sp.text_color,
                    ) if sp else None
                ),
            )

        result.append(ContentItemOut(
            id=c.id,
            community_id=c.community_id,
            type=c.type,
            title=c.title,
            body=body,
            event_date=c.event_date,
            media=[_media_to_out(m) for m in media],
            tags=tags,
            skills=[_skill_to_out(s) for s in skills],
            cost=c.cost,
            participant_payout=c.participant_payout,
        ))
    return result


@router.post("/posts", response_model=PostOut)
async def create_post(data: PostCreateIn, session: AsyncSession = Depends(get_session), user=Depends(role_required("company"))):
    uc = ContentUseCase(posts=PostRepo(session), stories=StoryRepo(session), media=MediaRepo(session))
    post = await uc.create_post(
        community_id=data.community_id,
        title=data.title,
        body=data.body,
        media_uids=data.media_uids or [],
        tags=data.tags,
        skill_ids=data.skill_ids,
        cost=data.cost,
        participant_payout=data.participant_payout,
    )
    # собрать media
    media = await MediaRepo(session).list_for_content(post.id)
    skills = await PostRepo(session).list_skills_for_post(post.id)
    def _skill_to_out(s) -> SkillOut:
        sp = getattr(s, "sphere", None)
        return SkillOut(
            id=s.id,
            title=s.title,
            sphere_id=s.sphere_id,
            sphere=(
                ContentSphereOut(
                    id=sp.id,
                    title=sp.title,
                    background_color=sp.background_color,
                    text_color=sp.text_color,
                ) if sp else None
            ),
        )

    return PostOut(
        id=post.id, community_id=post.community_id,
        title=post.title, body=post.body,
        media=[_media_to_out(m) for m in media],
        tags=post.tags,
        skills=[_skill_to_out(s) for s in skills],
        cost=post.cost,
        participant_payout=post.participant_payout,
    )


@router.patch("/posts/{post_id}", response_model=PostOut)
async def update_post(post_id: str, data: PostUpdateIn, session: AsyncSession = Depends(get_session),
                      user=Depends(role_required("company"))):
    uc = ContentUseCase(posts=PostRepo(session), stories=StoryRepo(session), media=MediaRepo(session))
    post = await uc.update_post(post_id, **data.model_dump(exclude_unset=True))
    media = await MediaRepo(session).list_for_content(post.id)
    skills = await PostRepo(session).list_skills_for_post(post.id)
    def _skill_to_out(s) -> SkillOut:
        sp = getattr(s, "sphere", None)
        return SkillOut(
            id=s.id,
            title=s.title,
            sphere_id=s.sphere_id,
            sphere=(
                ContentSphereOut(
                    id=sp.id,
                    title=sp.title,
                    background_color=sp.background_color,
                    text_color=sp.text_color,
                ) if sp else None
            ),
        )

    return PostOut(
        id=post.id, community_id=post.community_id,
        title=post.title, body=post.body,
        media=[_media_to_out(m) for m in media],
        tags=post.tags,
        skills=[_skill_to_out(s) for s in skills],
        cost=post.cost,
        participant_payout=post.participant_payout,
    )


@router.get("/posts/{post_id}", response_model=ContentItemOut)
async def get_post(post_id: str, session: AsyncSession = Depends(get_session)):
    # Load raw content row to preserve type-specific fields (event_date, description)
    row = (await session.execute(select(ContentModel).where(ContentModel.id == post_id))).scalar_one_or_none()
    if not row:
        raise HTTPException(404, "Not found")
    media_repo = MediaRepo(session)
    media = await media_repo.list_for_content(row.id)
    # Fallback: if no content_media links, try legacy single media_id field
    if not media and getattr(row, "media_id", None):
        m = await media_repo.get(row.media_id)
        if m:
            media = [m]
    # Build skills enriched with sphere (same as list)
    skills = await PostRepo(session).list_skills_for_post(row.id)
    def _skill_to_out(s) -> SkillOut:
        sp = getattr(s, "sphere", None)
        return SkillOut(
            id=s.id,
            title=s.title,
            sphere_id=s.sphere_id,
            sphere=(
                ContentSphereOut(
                    id=sp.id,
                    title=sp.title,
                    background_color=sp.background_color,
                    text_color=sp.text_color,
                ) if sp else None
            ),
        )
    # Unify body/event fields with list endpoint behavior
    body = row.body if row.type == "post" else (row.description or None)
    # Parse tags from comma-separated string for consistency
    tags = [t.strip() for t in (row.tags or "").split(",") if t.strip()]
    return ContentItemOut(
        id=row.id,
        community_id=row.community_id,
        type=row.type,
        title=row.title,
        body=body,
        event_date=row.event_date,
        media=[_media_to_out(m) for m in media],
        tags=tags,
        skills=[_skill_to_out(s) for s in skills],
        cost=row.cost,
        participant_payout=row.participant_payout,
    )


@router.post("/stories", response_model=StoryOut)
async def create_story(data: StoryCreateIn, session: AsyncSession = Depends(get_session),
                       user=Depends(role_required("company"))):
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


@router.get("/users/{user_id}/posts/featured", response_model=list[PostOut])
async def list_user_featured_posts(user_id: str, limit: int = 20, session: AsyncSession = Depends(get_session)):
    uc = ContentUseCase(posts=PostRepo(session), stories=StoryRepo(session), media=MediaRepo(session))
    posts = await uc.featured_posts_for_user(user_id=user_id, limit=limit)
    out: list[PostOut] = []
    for p in posts:
        media = await MediaRepo(session).list_for_content(p.id)
        skills = await PostRepo(session).list_skills_for_post(p.id)
        def _skill_to_out(s) -> SkillOut:
            sp = getattr(s, "sphere", None)
            return SkillOut(
                id=s.id,
                title=s.title,
                sphere_id=s.sphere_id,
                sphere=(
                    ContentSphereOut(
                        id=sp.id,
                        title=sp.title,
                        background_color=sp.background_color,
                        text_color=sp.text_color,
                    ) if sp else None
                ),
            )

        out.append(PostOut(
            id=p.id, community_id=p.community_id,
            title=p.title, body=p.body,
            media=[_media_to_out(m) for m in media],
            tags=p.tags,
            skills=[_skill_to_out(s) for s in skills],
            cost=p.cost,
            participant_payout=p.participant_payout,
        ))
    return out


@router.get("/me/posts/featured", response_model=list[PostOut])
async def list_my_featured_posts(limit: int = 20, session: AsyncSession = Depends(get_session),
                                 user=Depends(get_current_user)):
    uc = ContentUseCase(posts=PostRepo(session), stories=StoryRepo(session), media=MediaRepo(session))
    posts = await uc.featured_posts_for_user(user_id=user.id, limit=limit)
    out: list[PostOut] = []
    for p in posts:
        media = await MediaRepo(session).list_for_content(p.id)
        skills = await PostRepo(session).list_skills_for_post(p.id)
        def _skill_to_out(s) -> SkillOut:
            sp = getattr(s, "sphere", None)
            return SkillOut(
                id=s.id,
                title=s.title,
                sphere_id=s.sphere_id,
                sphere=(
                    ContentSphereOut(
                        id=sp.id,
                        title=sp.title,
                        background_color=sp.background_color,
                        text_color=sp.text_color,
                    ) if sp else None
                ),
            )

        out.append(PostOut(
            id=p.id, community_id=p.community_id,
            title=p.title, body=p.body,
            media=[_media_to_out(m) for m in media],
            tags=p.tags,
            skills=[_skill_to_out(s) for s in skills],
            cost=p.cost,
            participant_payout=p.participant_payout,
        ))
    return out


@router.get("/me/posts/from-followed-communities", response_model=list[PostOut])
async def posts_from_followed_communities(limit: int = 20, session: AsyncSession = Depends(get_session),
                                          user=Depends(get_current_user)):
    uc = ContentUseCase(posts=PostRepo(session), stories=StoryRepo(session), media=MediaRepo(session))
    posts = await uc.posts_from_followed_communities(user_id=user.id, limit=limit)
    out: list[PostOut] = []
    for p in posts:
        media = await MediaRepo(session).list_for_content(p.id)
        skills = await PostRepo(session).list_skills_for_post(p.id)
        def _skill_to_out(s) -> SkillOut:
            sp = getattr(s, "sphere", None)
            return SkillOut(
                id=s.id,
                title=s.title,
                sphere_id=s.sphere_id,
                sphere=(
                    ContentSphereOut(
                        id=sp.id,
                        title=sp.title,
                        background_color=sp.background_color,
                        text_color=sp.text_color,
                    ) if sp else None
                ),
            )

        out.append(PostOut(
            id=p.id, community_id=p.community_id,
            title=p.title, body=p.body,
            media=[_media_to_out(m) for m in media],
            tags=p.tags,
            skills=[_skill_to_out(s) for s in skills],
            cost=p.cost,
            participant_payout=p.participant_payout,
        ))
    return out


@router.get("/me/stories/from-followed-companies", response_model=list[StoryOut])
async def stories_from_followed_companies(limit: int = 20, session: AsyncSession = Depends(get_session),
                                          user=Depends(get_current_user)):
    uc = ContentUseCase(posts=PostRepo(session), stories=StoryRepo(session), media=MediaRepo(session),
                        company_follows=CompanyFollowRepo(session))
    stories = await uc.stories_for_followed_companies(user.id, limit)
    # Поскольку domain Story не содержит media_id, вернем только media_url
    return [
        StoryOut(id=s.id, community_id=s.company_id, title=s.title, media_url=s.media_url, media=None)
        for s in stories
    ]
