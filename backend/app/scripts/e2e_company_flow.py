"""
Company flow HTTP script against a running backend instance.

Actions:
- Company signup (unique email) to obtain bearer token
- Create a community (company-scoped)
- Upload media (multipart)
- Create a post with media in the community
- Create a story for the company with uploaded media
- Create an event in the community
- Verify created resources via GET/list endpoints

Usage:
  python -m app.scripts.e2e_company_flow --base-url http://91.197.99.176:8000

Optional args:
  --email test+<rand>@example.com
  --password <random>
  --company-name "Test Company <rand>"
  --verbose
"""

from __future__ import annotations

import argparse
import datetime as dt
import io
import os
import random
import string
import sys
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


DEFAULT_BASE_URL = "http://91.197.99.176:8000"


def _rand(n: int = 6) -> str:
    return "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(n))


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
    if resp.request.body and isinstance(resp.request.body, (str, bytes)):
        preview = resp.request.body if isinstance(resp.request.body, str) else b"<binary>"
        print(f"     req: {preview}")
    print(f"     status: {resp.status_code}")
    print(f"     resp: {body}")


def _headers(token: Optional[str] = None) -> Dict[str, str]:
    h = {}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def post(base: str, path: str, json: Dict[str, Any] | None = None, token: str | None = None, verbose: bool = False):
    url = base.rstrip("/") + path
    resp = requests.post(url, headers={"Content-Type": "application/json", **_headers(token)}, json=json, timeout=30)
    _maybe_verbose(resp, verbose)
    return resp


def get(base: str, path: str, params: Dict[str, Any] | None = None, token: str | None = None, verbose: bool = False):
    url = base.rstrip("/") + path
    resp = requests.get(url, headers=_headers(token), params=params, timeout=30)
    _maybe_verbose(resp, verbose)
    return resp


def patch(base: str, path: str, json: Dict[str, Any] | None = None, token: str | None = None, verbose: bool = False):
    url = base.rstrip("/") + path
    resp = requests.patch(url, headers={"Content-Type": "application/json", **_headers(token)}, json=json, timeout=30)
    _maybe_verbose(resp, verbose)
    return resp


def upload(base: str, filename: str, content: bytes, mime: str, token: str | None = None, verbose: bool = False):
    url = base.rstrip("/") + "/media/upload"
    files = {"file": (filename, io.BytesIO(content), mime)}
    resp = requests.post(url, headers=_headers(token), files=files, timeout=60)
    _maybe_verbose(resp, verbose)
    return resp


@dataclass
class Ctx:
    base_url: str
    token: Optional[str] = None
    company_id: Optional[str] = None
    community_id: Optional[str] = None
    post_id: Optional[str] = None
    story_id: Optional[str] = None
    event_id: Optional[str] = None
    company_name: Optional[str] = None


def step_company_signup(ctx: Ctx, email: str, password: str, name: str, verbose: bool) -> None:
    _log("[1/7] Company signup...")
    r = post(ctx.base_url, "/auth/company/signup", json={"email": email, "password": password, "name": name}, verbose=verbose)
    if r.status_code != 200:
        _log(f"ERROR: signup failed: {r.status_code} {r.text}")
        sys.exit(1)
    token = r.json().get("access_token")
    if not token:
        _log("ERROR: no access_token returned")
        sys.exit(1)
    ctx.token = token
    ctx.company_name = name
    _log("OK: received company token")


def step_resolve_company_id(ctx: Ctx, verbose: bool) -> None:
    _log("[2/7] Resolving company id...")
    r = get(ctx.base_url, "/companies", verbose=verbose)
    if r.status_code != 200:
        _log(f"ERROR: list companies failed: {r.status_code} {r.text}")
        sys.exit(1)
    companies = r.json()
    match = next((c for c in companies if c.get("name") == ctx.company_name), None)
    if not match:
        _log("ERROR: created company not found in listing")
        sys.exit(1)
    ctx.company_id = match.get("id")
    _log(f"OK: company_id={ctx.company_id}")


def step_create_community(ctx: Ctx, verbose: bool) -> None:
    _log("[3/7] Creating community...")
    payload = {
        "name": f"Community {_rand(4)}",
        "tags": "test,api,company-flow",
        "description": "Community created by e2e_company_flow",
        "telegram_url": None,
    }
    r = post(ctx.base_url, "/communities", json=payload, token=ctx.token, verbose=verbose)
    if r.status_code != 200:
        _log(f"ERROR: create community failed: {r.status_code} {r.text}")
        sys.exit(1)
    ctx.community_id = r.json().get("id")
    _log(f"OK: community_id={ctx.community_id}")


def _sample_png() -> bytes:
    # 1x1 transparent PNG
    return (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
        b"\x00\x00\x00\x0bIDAT\x08\x99c\x00\x01\x00\x00\x05\x00\x01\x0d\n\x2d\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
    )


def step_upload_media(ctx: Ctx, verbose: bool) -> tuple[str, str]:
    _log("[4/7] Uploading media (for post and story)...")
    r1 = upload(ctx.base_url, filename="post.png", content=_sample_png(), mime="image/png", token=ctx.token, verbose=verbose)
    if r1.status_code != 200:
        _log(f"ERROR: upload media (post) failed: {r1.status_code} {r1.text}")
        sys.exit(1)
    post_media_id = r1.json().get("id")

    r2 = upload(ctx.base_url, filename="story.png", content=_sample_png(), mime="image/png", token=ctx.token, verbose=verbose)
    if r2.status_code != 200:
        _log(f"ERROR: upload media (story) failed: {r2.status_code} {r2.text}")
        sys.exit(1)
    story_media_id = r2.json().get("id")

    _log(f"OK: media uploaded post_media={post_media_id}, story_media={story_media_id}")
    return post_media_id, story_media_id


def step_create_post(ctx: Ctx, media_uid: str, verbose: bool) -> None:
    _log("[5/7] Creating post in community...")
    payload = {
        "community_id": ctx.community_id,
        "title": f"Post {_rand(4)}",
        "body": "Post created via e2e_company_flow",
        "featured": True,
        "media_uids": [media_uid],
    }
    r = post(ctx.base_url, "/content/posts", json=payload, token=ctx.token, verbose=verbose)
    if r.status_code != 200:
        _log(f"ERROR: create post failed: {r.status_code} {r.text}")
        sys.exit(1)
    ctx.post_id = r.json().get("id")
    _log(f"OK: post_id={ctx.post_id}")


def step_create_story(ctx: Ctx, media_uid: str, verbose: bool) -> None:
    _log("[6/7] Creating story for company...")
    payload = {
        "company_id": ctx.company_id,
        "title": f"Story {_rand(4)}",
        "media_uid": media_uid,
    }
    r = post(ctx.base_url, "/content/stories", json=payload, token=ctx.token, verbose=verbose)
    if r.status_code != 200:
        _log(f"ERROR: create story failed: {r.status_code} {r.text}")
        sys.exit(1)
    ctx.story_id = r.json().get("id")
    _log(f"OK: story_id={ctx.story_id}")


def step_create_event(ctx: Ctx, verbose: bool) -> None:
    _log("[7/7] Creating event for community...")
    starts_at = (dt.datetime.utcnow() + dt.timedelta(days=3)).replace(microsecond=0).isoformat() + "Z"
    payload = {
        "community_id": ctx.community_id,
        "title": f"Event {_rand(4)}",
        "starts_at": starts_at,
        "city": "Moscow",
        "location": "Online",
        "description": "Event created by e2e_company_flow",
        "registration": "https://example.com/register",
        "format": "online",
        # media_id: optional, omit
    }
    r = post(ctx.base_url, "/events", json=payload, token=ctx.token, verbose=verbose)
    if r.status_code != 200:
        _log(f"ERROR: create event failed: {r.status_code} {r.text}")
        sys.exit(1)
    # Events API returns created event object; capture id if present
    ctx.event_id = r.json().get("id")
    _log(f"OK: event created id={ctx.event_id}")

    # Quick verifications
    _log("Verifying resources...")
    if ctx.post_id:
        rp = get(ctx.base_url, f"/content/posts/{ctx.post_id}", token=None, verbose=verbose)
        _log(f"Post GET status: {rp.status_code}")
    if ctx.story_id:
        rs = get(ctx.base_url, f"/content/stories/{ctx.story_id}", token=None, verbose=verbose)
        _log(f"Story GET status: {rs.status_code}")
    # list posts in the community
    rc = get(ctx.base_url, f"/communities/{ctx.community_id}/posts", token=None, verbose=verbose)
    _log(f"Community posts status: {rc.status_code}")
    # upcoming events visible to company user
    re = get(ctx.base_url, "/events/my/upcoming", token=ctx.token, verbose=verbose)
    _log(f"My upcoming events: {re.status_code}")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Company flow HTTP script")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="Service base URL")
    parser.add_argument("--email", default=None, help="Company email (default: random @example.com)")
    parser.add_argument("--password", default=None, help="Password (default: random)")
    parser.add_argument("--company-name", default=None, help="Company name (default: random)")
    parser.add_argument("--verbose", action="store_true", help="Verbose HTTP logs")
    args = parser.parse_args(argv)

    email = args.email or f"test+{_rand(8)}@example.com"
    password = args.password or ("A1" + _rand(10))
    company_name = args.company_name or f"API Test Company {_rand(6)}"

    ctx = Ctx(base_url=args.base_url)

    _log(f"Base URL: {ctx.base_url}")
    _log(f"Email: {email}")
    _log(f"Company: {company_name}")

    step_company_signup(ctx, email=email, password=password, name=company_name, verbose=args.verbose)
    step_resolve_company_id(ctx, verbose=args.verbose)
    step_create_community(ctx, verbose=args.verbose)
    post_media_uid, story_media_uid = step_upload_media(ctx, verbose=args.verbose)
    step_create_post(ctx, media_uid=post_media_uid, verbose=args.verbose)
    step_create_story(ctx, media_uid=story_media_uid, verbose=args.verbose)
    step_create_event(ctx, verbose=args.verbose)

    _log("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

