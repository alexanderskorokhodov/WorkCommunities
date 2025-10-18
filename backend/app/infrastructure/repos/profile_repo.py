from typing import Optional, Sequence

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import Profile, Skill, Sphere, Status
from app.domain.repositories import IProfileRepo
from .sql_models import (
    ProfileModel,
    ProfileSkillModel,
    ProfileStatusModel,
    SkillModel,
    SphereModel,
    StatusModel,
)


def _profile_from_row(m: ProfileModel) -> Profile:
    return Profile(
        id=m.id,
        user_id=m.user_id,
        full_name=m.full_name,
        portfolio_url=m.portfolio_url,
        description=m.description,
        skills=[],
        statuses=[],
    )


def _sphere_from_row(m: SphereModel) -> Sphere:
    return Sphere(id=m.id, title=m.title, background_color=m.background_color, text_color=m.text_color)


def _skill_from_row(m: SkillModel, sphere: Optional[Sphere] = None) -> Skill:
    return Skill(id=m.id, title=m.title, sphere_id=m.sphere_id, sphere=sphere)


def _status_from_row(m: StatusModel) -> Status:
    return Status(id=m.id, title=m.title)


class ProfileRepo(IProfileRepo):
    def __init__(self, s: AsyncSession):
        self.s = s

    async def _attach_relations(self, profile: Profile) -> Profile:
        # skills with spheres
        ps_res = await self.s.execute(select(ProfileSkillModel).where(ProfileSkillModel.profile_id == profile.id))
        profile_skill_rows: Sequence[ProfileSkillModel] = ps_res.scalars().all()
        skill_ids = [r.skill_id for r in profile_skill_rows]
        skills: list[Skill] = []
        if skill_ids:
            sk_res = await self.s.execute(select(SkillModel).where(SkillModel.id.in_(skill_ids)))
            skill_models = {sm.id: sm for sm in sk_res.scalars().all()}
            sphere_ids = list({sm.sphere_id for sm in skill_models.values()})
            sp_map: dict[str, Sphere] = {}
            if sphere_ids:
                sp_res = await self.s.execute(select(SphereModel).where(SphereModel.id.in_(sphere_ids)))
                sp_map = {sp.id: _sphere_from_row(sp) for sp in sp_res.scalars().all()}
            for sid in skill_ids:
                sm = skill_models.get(sid)
                if sm:
                    sphere = sp_map.get(sm.sphere_id)
                    skills.append(_skill_from_row(sm, sphere))
        profile.skills = skills

        # statuses
        pst_res = await self.s.execute(select(ProfileStatusModel).where(ProfileStatusModel.profile_id == profile.id))
        profile_status_rows: Sequence[ProfileStatusModel] = pst_res.scalars().all()
        status_ids = [r.status_id for r in profile_status_rows]
        statuses: list[Status] = []
        if status_ids:
            st_res = await self.s.execute(select(StatusModel).where(StatusModel.id.in_(status_ids)))
            statuses = [_status_from_row(st) for st in st_res.scalars().all()]
        profile.statuses = statuses
        return profile

    async def create(self, user_id: str, **data) -> Profile:
        m = ProfileModel(
            user_id=user_id,
            full_name=data.get("full_name"),
            portfolio_url=data.get("portfolio_url"),
            description=data.get("description"),
            # keep DB columns city/interests untouched; they may exist but are deprecated in API
        )
        self.s.add(m)
        await self.s.flush()
        p = _profile_from_row(m)
        return await self._attach_relations(p)

    async def get(self, profile_id: str) -> Optional[Profile]:
        res = await self.s.execute(select(ProfileModel).where(ProfileModel.id == profile_id))
        row = res.scalar_one_or_none()
        if not row:
            return None
        p = _profile_from_row(row)
        return await self._attach_relations(p)

    async def get_by_user_id(self, user_id: str) -> Optional[Profile]:
        res = await self.s.execute(select(ProfileModel).where(ProfileModel.user_id == user_id))
        row = res.scalar_one_or_none()
        if not row:
            return None
        p = _profile_from_row(row)
        return await self._attach_relations(p)

    async def get_or_create_for_user(self, user_id: str) -> Profile:
        existing = await self.get_by_user_id(user_id)
        if existing:
            return existing
        return await self.create(user_id)

    async def update(self, user_id: str, **data) -> Profile:
        # find existing profile or create
        prof = await self.get_by_user_id(user_id)
        if not prof:
            prof = await self.create(user_id)

        update_data = data.copy()

        # pop relation updates
        skill_uids = update_data.pop("skill_uids", None)
        status_uids = update_data.pop("status_uids", None)

        # update scalar fields
        await self.s.execute(
            update(ProfileModel).where(ProfileModel.id == prof.id).values(**update_data)
        )

        # validate and replace skills if provided
        if skill_uids is not None:
            # normalize: strip, drop empty, deduplicate keeping order
            cleaned_skill_uids: list[str] = []
            seen = set()
            for sid in (sid or "" for sid in skill_uids):
                sid = sid.strip()
                if not sid:
                    continue
                if sid not in seen:
                    cleaned_skill_uids.append(sid)
                    seen.add(sid)

            if cleaned_skill_uids:
                # validate existence in skills table
                sk_res = await self.s.execute(select(SkillModel.id).where(SkillModel.id.in_(cleaned_skill_uids)))
                found_ids = {row[0] for row in sk_res.all()}
                missing = [sid for sid in cleaned_skill_uids if sid not in found_ids]
                if missing:
                    # do not update if any invalid ids
                    raise ValueError(f"Invalid skill_uids: {', '.join(missing)}")

            # perform replacement (clear if empty)
            await self.s.execute(delete(ProfileSkillModel).where(ProfileSkillModel.profile_id == prof.id))
            for sid in cleaned_skill_uids:
                self.s.add(ProfileSkillModel(profile_id=prof.id, skill_id=sid))

        # validate and replace statuses if provided
        if status_uids is not None:
            # normalize: strip, drop empty, deduplicate keeping order
            cleaned_status_uids: list[str] = []
            seen_st = set()
            for stid in (stid or "" for stid in status_uids):
                stid = stid.strip()
                if not stid:
                    continue
                if stid not in seen_st:
                    cleaned_status_uids.append(stid)
                    seen_st.add(stid)

            if cleaned_status_uids:
                # validate existence in statuses table
                st_res = await self.s.execute(select(StatusModel.id).where(StatusModel.id.in_(cleaned_status_uids)))
                found_st = {row[0] for row in st_res.all()}
                missing_st = [stid for stid in cleaned_status_uids if stid not in found_st]
                if missing_st:
                    raise ValueError(f"Invalid status_uids: {', '.join(missing_st)}")

            # perform replacement (clear if empty)
            await self.s.execute(delete(ProfileStatusModel).where(ProfileStatusModel.profile_id == prof.id))
            for stid in cleaned_status_uids:
                self.s.add(ProfileStatusModel(profile_id=prof.id, status_id=stid))

        await self.s.flush()
        # reload
        return await self.get(prof.id)
