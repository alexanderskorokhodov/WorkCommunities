from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.db import get_session
from app.core.deps import get_current_user, role_required, get_current_company
from app.infrastructure.repos.community_repo import CommunityRepo
from app.infrastructure.repos.follow_repo import FollowRepo
from app.infrastructure.repos.post_repo import PostRepo
from app.infrastructure.repos.media_repo import MediaRepo
from app.presentation.schemas.communities import CommunityOut, CommunityCreateIn, CommunityUpdateIn
from app.presentation.schemas.content import PostOut, MediaOut
from app.usecases.communities import CommunityUseCase

router = APIRouter()


@router.get("/mine", response_model=list[CommunityOut])
async def list_my_communities(
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    repo = CommunityRepo(session)
    items = await repo.list_for_user(user.id)
    return [
        CommunityOut(
            id=i.id,
            company_id=i.company_id,
            name=i.name,
            description=i.description,
            telegram_url=i.telegram_url,
            tags=i.tags,
            is_archived=i.is_archived,
        )
        for i in items
    ]


@router.get("/joinable", response_model=list[CommunityOut])
async def list_joinable_communities(
    offset: int = 0,
    limit: int = 20,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    repo = CommunityRepo(session)
    items = await repo.list_joinable(user.id, offset=offset, limit=limit)
    return [
        CommunityOut(
            id=i.id,
            company_id=i.company_id,
            name=i.name,
            description=i.description,
            telegram_url=i.telegram_url,
            tags=i.tags,
            is_archived=i.is_archived,
        )
        for i in items
    ]

@router.get("/", response_model=list[CommunityOut])
async def list_communities(session: AsyncSession = Depends(get_session)):
    repo = CommunityRepo(session)
    items = await repo.list_all()
    return [
        CommunityOut(
            id=i.id,
            company_id=i.company_id,
            name=i.name,
            description=i.description,
            telegram_url=i.telegram_url,
            tags=i.tags,
            is_archived=i.is_archived,
        )
        for i in items
    ]


@router.get("/by-company/{company_id}", response_model=list[CommunityOut])
async def list_company_communities(company_id: str, session: AsyncSession = Depends(get_session)):
    repo = CommunityRepo(session)
    items = await repo.list_for_company(company_id)
    return [
        CommunityOut(
            id=i.id,
            company_id=i.company_id,
            name=i.name,
            description=i.description,
            telegram_url=i.telegram_url,
            tags=i.tags,
            is_archived=i.is_archived,
        )
        for i in items
    ]


@router.post("/", response_model=CommunityOut)
async def create_community(
    data: CommunityCreateIn,
    session: AsyncSession = Depends(get_session),
    company=Depends(get_current_company),
):
    uc = CommunityUseCase(communities=CommunityRepo(session), members=None, follows=FollowRepo(session))
    c = await uc.create(
        name=data.name,
        company_id=company.id,
        tags=data.tags,
        description=data.description,
        telegram_url=data.telegram_url,
    )
    return CommunityOut(
        id=c.id,
        company_id=c.company_id,
        name=c.name,
        description=c.description,
        telegram_url=c.telegram_url,
        tags=c.tags,
        is_archived=c.is_archived,
    )


@router.patch("/{community_id}", response_model=CommunityOut, dependencies=[Depends(role_required("company"))])
async def update_community(community_id: str, data: CommunityUpdateIn, session: AsyncSession = Depends(get_session)):
    uc = CommunityUseCase(communities=CommunityRepo(session), members=None, follows=FollowRepo(session))
    c = await uc.update(community_id, **data.model_dump(exclude_unset=True))
    if not c:
        raise HTTPException(404, "Not found")
    return CommunityOut(
        id=c.id,
        company_id=c.company_id,
        name=c.name,
        description=c.description,
        telegram_url=c.telegram_url,
        tags=c.tags,
        is_archived=c.is_archived,
    )


@router.post("/{community_id}/follow")
async def follow_community(community_id: str, session: AsyncSession = Depends(get_session), user=Depends(get_current_user)):
    uc = CommunityUseCase(communities=CommunityRepo(session), members=None, follows=FollowRepo(session))
    await uc.follow(user.id, community_id)
    return {"status": "ok"}


@router.delete("/{community_id}/follow")
async def unfollow_community(community_id: str, session: AsyncSession = Depends(get_session), user=Depends(get_current_user)):
    uc = CommunityUseCase(communities=CommunityRepo(session), members=None, follows=FollowRepo(session))
    await uc.unfollow(user.id, community_id)
    return {"status": "ok"}


@router.get("/{community_id}/posts", response_model=list[PostOut])
async def list_community_posts(
    community_id: str,
    offset: int = 0,
    limit: int = 20,
    session: AsyncSession = Depends(get_session),
):
    posts = await PostRepo(session).list_for_community(community_id, offset=offset, limit=limit)
    media_repo = MediaRepo(session)

    def _media_to_out(m) -> MediaOut:
        kind = m.kind.value if hasattr(m.kind, "value") else m.kind
        return MediaOut(id=m.id, kind=kind, mime=m.mime, ext=m.ext, size=m.size, url=m.url)

    result: list[PostOut] = []
    for p in posts:
        media = await media_repo.list_for_post(p.id)
        result.append(PostOut(
            id=p.id,
            community_id=p.community_id,
            author_user_id=p.author_user_id,
            title=p.title,
            body=p.body,
            featured=p.featured,
            media=[_media_to_out(m) for m in media],
        ))
    return result
