"""
End-to-end HTTP sanity test against a running backend instance.

It exercises:
- Auth via OTP (creates a student user on first login)
- Profile fetch and update
- Communities list, follow, and posts fetch
- Events listing and joining
- Content feed from followed communities

Usage:
  python -m app.scripts.e2e_http_test --base-url http://91.197.99.176:8000

Optional args:
  --phone +7999XXXXXXXX  Use a specific phone (default: random)
  --code 11111           OTP code (default: 11111)
  --verbose              Print verbose HTTP details

Note: This script only performs HTTP requests to a running service; it does not
require the repo to be running locally. Ensure the base URL is reachable.
"""

from __future__ import annotations

import argparse
import random
import string
import sys
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


DEFAULT_BASE_URL = "http://91.197.99.176:8000"


def _rand_phone() -> str:
    # E.164-like: +7 then 10 digits
    digits = "7" + "".join(random.choice(string.digits) for _ in range(10))
    return "+" + digits


def _log(msg: str) -> None:
    print(msg)


def _maybe_verbose(resp: requests.Response, verbose: bool) -> None:
    if not verbose:
        return
    try:
        body = resp.json()
    except Exception:
        body = resp.text
    print(f"  -> {resp.request.method} {resp.request.url}")
    if resp.request.body:
        print(f"     req: {resp.request.body}")
    print(f"     status: {resp.status_code}")
    print(f"     resp: {body}")


def _headers(token: Optional[str] = None) -> Dict[str, str]:
    h = {"Content-Type": "application/json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def post(base: str, path: str, json: Dict[str, Any] | None = None, token: str | None = None, verbose: bool = False):
    url = base.rstrip("/") + path
    resp = requests.post(url, headers=_headers(token), json=json, timeout=30)
    _maybe_verbose(resp, verbose)
    return resp


def get(base: str, path: str, params: Dict[str, Any] | None = None, token: str | None = None, verbose: bool = False):
    url = base.rstrip("/") + path
    resp = requests.get(url, headers=_headers(token), params=params, timeout=30)
    _maybe_verbose(resp, verbose)
    return resp


def patch(base: str, path: str, json: Dict[str, Any] | None = None, token: str | None = None, verbose: bool = False):
    url = base.rstrip("/") + path
    resp = requests.patch(url, headers=_headers(token), json=json, timeout=30)
    _maybe_verbose(resp, verbose)
    return resp


@dataclass
class TestContext:
    base_url: str
    token: Optional[str] = None
    user_id: Optional[str] = None
    phone: Optional[str] = None


def step_auth_create_user(ctx: TestContext, phone: str, code: str, verbose: bool) -> None:
    _log("[1/7] Requesting OTP...")
    r = post(ctx.base_url, "/auth/otp/request", json={"phone": phone}, verbose=verbose)
    if r.status_code not in (200, 204):
        _log(f"ERROR: OTP request failed: {r.status_code} {r.text}")
        sys.exit(1)

    _log("Verifying OTP (creates user if not exists)...")
    r = post(ctx.base_url, "/auth/otp/verify", json={"phone": phone, "code": code}, verbose=verbose)
    if r.status_code != 200:
        _log(f"ERROR: OTP verify failed: {r.status_code} {r.text}")
        sys.exit(1)
    token = r.json().get("access_token")
    if not token:
        _log("ERROR: access_token missing in response")
        sys.exit(1)
    ctx.token = token
    ctx.phone = phone
    _log("OK: received access token")


def step_fetch_profile(ctx: TestContext, verbose: bool) -> Dict[str, Any]:
    _log("[2/7] Fetching my profile...")
    r = get(ctx.base_url, "/profiles/me", token=ctx.token, verbose=verbose)
    if r.status_code != 200:
        _log(f"ERROR: Get profile failed: {r.status_code} {r.text}")
        sys.exit(1)
    prof = r.json()
    ctx.user_id = prof.get("user_id")
    _log(f"OK: profile id={prof.get('id')} user_id={ctx.user_id}")
    return prof


def step_update_profile(ctx: TestContext, verbose: bool) -> Dict[str, Any]:
    _log("[3/7] Updating profile...")
    # Fetch skills and statuses to pick valid IDs
    skills = get(ctx.base_url, "/reference/skills", verbose=verbose)
    statuses = get(ctx.base_url, "/reference/statuses", verbose=verbose)
    skill_ids = [s["id"] for s in (skills.json() if skills.status_code == 200 else [])]
    status_ids = [s["id"] for s in (statuses.json() if statuses.status_code == 200 else [])]

    payload: Dict[str, Any] = {
        "full_name": "Test User",
        "portfolio_url": "https://example.com/portfolio",
        "description": "Automated test profile update",
    }
    if skill_ids:
        payload["skill_uids"] = skill_ids[:2]
    if status_ids:
        payload["status_uids"] = status_ids[:1]

    r = patch(ctx.base_url, "/profiles/me", json=payload, token=ctx.token, verbose=verbose)
    if r.status_code != 200:
        _log(f"ERROR: Update profile failed: {r.status_code} {r.text}")
        sys.exit(1)
    _log("OK: profile updated")
    return r.json()


def step_communities_and_posts(ctx: TestContext, verbose: bool) -> None:
    _log("[4/7] Listing communities and following one...")
    # Public list
    r_all = get(ctx.base_url, "/communities", verbose=verbose)
    communities = r_all.json() if r_all.status_code == 200 else []
    total = len(communities)
    _log(f"Communities available: {total}")

    # Joinable for this user
    r_joinable = get(ctx.base_url, "/communities/joinable", token=ctx.token, verbose=verbose)
    joinable = r_joinable.json() if r_joinable.status_code == 200 else []
    if joinable:
        cid = joinable[0]["id"]
        _log(f"Following community {cid}...")
        r_follow = post(ctx.base_url, f"/communities/{cid}/follow", token=ctx.token, json={}, verbose=verbose)
        if r_follow.status_code not in (200, 204):
            _log(f"WARN: Follow failed: {r_follow.status_code} {r_follow.text}")
        else:
            _log("OK: followed")
    else:
        _log("WARN: No joinable communities for this user")

    # Pick a community to check posts
    target_c = (joinable or communities)
    if not target_c:
        _log("WARN: No communities to inspect posts")
        return
    cid = target_c[0]["id"]
    _log(f"Fetching posts for community {cid}...")
    r_posts = get(ctx.base_url, f"/communities/{cid}/posts", verbose=verbose)
    if r_posts.status_code != 200:
        _log(f"WARN: Posts fetch failed: {r_posts.status_code} {r_posts.text}")
        return
    posts = r_posts.json()
    _log(f"Posts found: {len(posts)}")


def step_events(ctx: TestContext, verbose: bool) -> None:
    _log("[5/7] Listing upcoming events...")
    r = get(ctx.base_url, "/events/upcoming", token=ctx.token, verbose=verbose)
    if r.status_code != 200:
        _log(f"WARN: Could not fetch events: {r.status_code} {r.text}")
        return
    events = r.json()
    _log(f"Upcoming events: {len(events)}")
    if not events:
        return
    eid = events[0]["id"]
    _log(f"Joining event {eid}...")
    rj = post(ctx.base_url, f"/events/{eid}/join", token=ctx.token, json={}, verbose=verbose)
    if rj.status_code not in (200, 204):
        _log(f"WARN: Join event failed: {rj.status_code} {rj.text}")
    else:
        _log("OK: joined event")


def step_feed(ctx: TestContext, verbose: bool) -> None:
    _log("[6/7] Fetching posts from followed communities...")
    r = get(ctx.base_url, "/content/me/posts/from-followed-communities", token=ctx.token, verbose=verbose)
    if r.status_code != 200:
        _log(f"WARN: Could not fetch feed: {r.status_code} {r.text}")
        return
    posts = r.json()
    _log(f"Feed posts: {len(posts)}")


def step_verify_profile(ctx: TestContext, verbose: bool) -> None:
    _log("[7/7] Verifying profile reflects updates...")
    r = get(ctx.base_url, "/profiles/me", token=ctx.token, verbose=verbose)
    if r.status_code != 200:
        _log(f"WARN: Could not re-fetch profile: {r.status_code} {r.text}")
        return
    prof = r.json()
    name = prof.get("full_name")
    if name == "Test User":
        _log("OK: profile update verified")
    else:
        _log("WARN: profile update not reflected as expected")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="E2E HTTP test for Communities API")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="Service base URL")
    parser.add_argument("--phone", default=None, help="Phone in +E164 format; default: random")
    parser.add_argument("--code", default="11111", help="OTP code; default 11111")
    parser.add_argument("--verbose", action="store_true", help="Verbose HTTP logging")
    args = parser.parse_args(argv)

    ctx = TestContext(base_url=args.base_url)
    phone = args.phone or _rand_phone()
    _log(f"Base URL: {ctx.base_url}")
    _log(f"Phone: {phone}")

    step_auth_create_user(ctx, phone=phone, code=args.code, verbose=args.verbose)
    step_fetch_profile(ctx, verbose=args.verbose)
    step_update_profile(ctx, verbose=args.verbose)
    step_communities_and_posts(ctx, verbose=args.verbose)
    step_events(ctx, verbose=args.verbose)
    step_feed(ctx, verbose=args.verbose)
    step_verify_profile(ctx, verbose=args.verbose)

    _log("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

