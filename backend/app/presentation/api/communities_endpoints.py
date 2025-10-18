from fastapi import APIRouter, Depends, HTTPException
import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.db import get_session
from app.core.deps import get_current_user, role_required, get_current_company, bearer
from app.core.config import settings
from app.infrastructure.repos.community_repo import CommunityRepo
from app.infrastructure.repos.follow_repo import FollowRepo
from app.infrastructure.repos.company_repo import CompanyRepo
from app.infrastructure.repos.post_repo import PostRepo
from app.infrastructure.repos.case_repo import CaseRepo
from app.infrastructure.repos.media_repo import MediaRepo
from app.presentation.schemas.communities import (
    CommunityOut,
    CommunityCreateIn,
    CommunityUpdateIn,
    CommunityWithMembersOut,
    CommunityDetailOut,
)
from app.presentation.schemas.cases import CaseOut, CaseCreateIn
from app.presentation.schemas.content import PostOut, MediaOut, SkillOut, ContentSphereOut
from app.usecases.communities import CommunityUseCase
from app.infrastructure.repos.membership_repo import MembershipRepo
from app.infrastructure.repos.user_repo import UserRepo

router = APIRouter()


@router.get("/mine", response_model=list[CommunityOut])
async def list_my_communities(
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
    creds = Depends(bearer),
):
    c_repo = CommunityRepo(session)
    # If company user — return communities of this company
    if user.role == "company":
        crepo = CompanyRepo(session)
        company = await crepo.get_by_owner(user.id)
        if not company and creds:
            try:
                payload = jwt.decode(creds.credentials, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
                company_id = payload.get("company_id")
                if company_id:
                    company = await crepo.get(company_id)
            except Exception:
                company = None
        if not company:
            raise HTTPException(status_code=403, detail="Company is not set for this user")
        items = await c_repo.list_for_company(company.id)
    else:
        # Regular user — return followed communities
        follow_ids = await FollowRepo(session).list_community_ids_for_user(user.id)
        items = await c_repo.list_by_ids(follow_ids)
    return [
        CommunityOut(
            id=i.id,
            company_id=i.company_id,
            name=i.name,
            description=i.description,
            telegram_url=i.telegram_url,
            tags=i.tags,
            is_archived=i.is_archived,
            logo_media_id=i.logo_media_id,
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
            logo_media_id=i.logo_media_id,
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
            logo_media_id=i.logo_media_id,
        )
        for i in items
    ]


@router.get("/by-company/{company_id}", response_model=list[CommunityOut])
async def list_company_communities(company_id: str, session: AsyncSession = Depends(get_session)):
    repo = CommunityRepo(session)
    items = await repo.list_for_company(company_id)
    # Compute members count per community
    ids = [i.id for i in items]
    counts = await MembershipRepo(session).counts_for_communities(ids)
    return [
        CommunityOut(
            id=i.id,
            company_id=i.company_id,
            name=i.name,
            description=i.description,
            telegram_url=i.telegram_url,
            tags=i.tags,
            is_archived=i.is_archived,
            logo_media_id=i.logo_media_id,
            members_count=counts.get(i.id, 0),
        )
        for i in items
    ]


@router.get("/{community_id}", response_model=CommunityDetailOut)
async def get_community_detail(community_id: str, session: AsyncSession = Depends(get_session)):
    c_repo = CommunityRepo(session)
    community = await c_repo.get(community_id)
    if not community:
        raise HTTPException(404, "Not found")

    # Cases
    cases = await CaseRepo(session).list_for_community(community_id)

    # Members
    member_ids = await MembershipRepo(session).list_user_ids_for_community(community_id)
    users: list = []
    if member_ids:
        urepo = UserRepo(session)
        for uid in member_ids:
            u = await urepo.get_by_id(uid)
            if u:
                users.append(u)

    return CommunityDetailOut(
        id=community.id,
        company_id=community.company_id,
        name=community.name,
        description=community.description,
        telegram_url=community.telegram_url,
        tags=community.tags,
        is_archived=community.is_archived,
        logo_media_id=community.logo_media_id,
        cases=[
            CaseOut(
                id=cs.id,
                community_id=cs.community_id,
                title=cs.title,
                description=cs.description,
                date=cs.date,
                solutions_count=cs.solutions_count,
            )
            for cs in cases
        ],
        members=[
            {
                "id": u.id,
                "role": u.role,
                "phone": u.phone,
                "email": u.email,
                "avatar_media_id": u.avatar_media_id,
                "created_at": u.created_at,
            }
            for u in users
        ],
    )


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
        logo_media_id=data.logo_media_id,
    )
    return CommunityOut(
        id=c.id,
        company_id=c.company_id,
        name=c.name,
        description=c.description,
        telegram_url=c.telegram_url,
        tags=c.tags,
        is_archived=c.is_archived,
        logo_media_id=c.logo_media_id,
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
        logo_media_id=c.logo_media_id,
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
        media = await media_repo.list_for_content(p.id)
        # load skills with sphere colors
        skills = await PostRepo(session).list_skills_for_post(p.id)
        def _skill_to_out(s) -> SkillOut:
            sp = getattr(s, "sphere", None)
            return SkillOut(
                id=s.id,
                title=s.title,
                sphere_id=s.sphere_id,
                sphere=(ContentSphereOut(
                    id=sp.id,
                    title=sp.title,
                    background_color=sp.background_color,
                    text_color=sp.text_color,
                ) if sp else None),
            )
        result.append(PostOut(
            id=p.id,
            community_id=p.community_id,
            title=p.title,
            body=p.body,
            media=[_media_to_out(m) for m in media],
            tags=p.tags,
            skills=[_skill_to_out(s) for s in skills],
            cost=p.cost,
            participant_payout=p.participant_payout,
        ))
    return result


@router.post("/{community_id}/cases", response_model=CaseOut, dependencies=[Depends(role_required("company"))])
async def create_case(
    community_id: str,
    data: CaseCreateIn,
    session: AsyncSession = Depends(get_session),
    company=Depends(get_current_company),
):
    # ensure community belongs to this company
    c = await CommunityRepo(session).get(community_id)
    if not c or c.company_id != company.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    cs = await CaseRepo(session).create(
        community_id=community_id,
        title=data.title,
        description=data.description,
        date=data.date,
        solutions_count=data.solutions_count,
    )
    return CaseOut(
        id=cs.id,
        community_id=cs.community_id,
        title=cs.title,
        description=cs.description,
        date=cs.date,
        solutions_count=cs.solutions_count,
    )


@router.delete("/{community_id}/cases/{case_id}", dependencies=[Depends(role_required("company"))])
async def delete_case(
    community_id: str,
    case_id: str,
    session: AsyncSession = Depends(get_session),
    company=Depends(get_current_company),
):
    c = await CommunityRepo(session).get(community_id)
    if not c or c.company_id != company.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    case = await CaseRepo(session).get_by_id(case_id)
    if not case or case.community_id != community_id:
        raise HTTPException(status_code=404, detail="Case not found")
    await CaseRepo(session).delete(case_id)
    return {"status": "ok"}


# Removed duplicate GET /{community_id} that previously returned members-only
