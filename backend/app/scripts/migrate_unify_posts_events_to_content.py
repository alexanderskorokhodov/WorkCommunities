"""
Migration: unify posts and events into a single `content` table with type field.

Actions:
- Create tables: content, content_media, content_skills (idempotent)
- Migrate data from posts -> content(type='post')
- Migrate data from events -> content(type='event') with event_date set from starts_at
- Migrate post_media -> content_media (same ids)
- Update event_participants to reference content (rename column + FK) if present

Usage (Docker):
  docker compose exec api python -m app.scripts.migrate_unify_posts_events_to_content

Safe to run multiple times.
"""

import asyncio
from sqlalchemy import text

from app.adapters.db import engine


CREATE_CONTENT_PG = """
CREATE TABLE IF NOT EXISTS content (
    id VARCHAR PRIMARY KEY,
    community_id VARCHAR NOT NULL REFERENCES communities(id),
    type VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    body TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    event_date TIMESTAMP NULL,
    city VARCHAR NULL,
    location VARCHAR NULL,
    description TEXT NULL,
    registration VARCHAR NULL,
    format VARCHAR NULL,
    media_id VARCHAR NULL REFERENCES media(id),
    tags TEXT NULL,
    cost INTEGER NULL,
    participant_payout INTEGER NULL
);
CREATE INDEX IF NOT EXISTS ix_content_type ON content(type);
CREATE INDEX IF NOT EXISTS ix_content_community ON content(community_id);
CREATE INDEX IF NOT EXISTS ix_content_event_date ON content(event_date);
"""

CREATE_CONTENT_SQLITE = """
CREATE TABLE IF NOT EXISTS content (
    id TEXT PRIMARY KEY,
    community_id TEXT NOT NULL,
    type TEXT NOT NULL,
    title TEXT NOT NULL,
    body TEXT NULL,
    created_at TEXT NOT NULL,
    event_date TEXT NULL,
    city TEXT NULL,
    location TEXT NULL,
    description TEXT NULL,
    registration TEXT NULL,
    format TEXT NULL,
    media_id TEXT NULL,
    tags TEXT NULL,
    cost INTEGER NULL,
    participant_payout INTEGER NULL
);
CREATE INDEX IF NOT EXISTS ix_content_type ON content(type);
CREATE INDEX IF NOT EXISTS ix_content_community ON content(community_id);
CREATE INDEX IF NOT EXISTS ix_content_event_date ON content(event_date);
"""

CREATE_CONTENT_MEDIA_PG = """
CREATE TABLE IF NOT EXISTS content_media (
    id VARCHAR PRIMARY KEY,
    content_id VARCHAR NOT NULL REFERENCES content(id),
    media_id VARCHAR NOT NULL REFERENCES media(id),
    order_index INTEGER NOT NULL DEFAULT 0,
    CONSTRAINT uq_content_media UNIQUE (content_id, media_id)
);
CREATE INDEX IF NOT EXISTS ix_content_media_content ON content_media(content_id);
CREATE INDEX IF NOT EXISTS ix_content_media_media ON content_media(media_id);
"""

CREATE_CONTENT_MEDIA_SQLITE = """
CREATE TABLE IF NOT EXISTS content_media (
    id TEXT PRIMARY KEY,
    content_id TEXT NOT NULL,
    media_id TEXT NOT NULL,
    order_index INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS ix_content_media_content ON content_media(content_id);
CREATE INDEX IF NOT EXISTS ix_content_media_media ON content_media(media_id);
"""

CREATE_CONTENT_SKILLS_PG = """
CREATE TABLE IF NOT EXISTS content_skills (
    id VARCHAR PRIMARY KEY,
    content_id VARCHAR NOT NULL REFERENCES content(id),
    skill_id VARCHAR NOT NULL REFERENCES skills(id),
    CONSTRAINT uq_content_skill UNIQUE (content_id, skill_id)
);
CREATE INDEX IF NOT EXISTS ix_content_skills_content ON content_skills(content_id);
CREATE INDEX IF NOT EXISTS ix_content_skills_skill ON content_skills(skill_id);
"""

CREATE_CONTENT_SKILLS_SQLITE = """
CREATE TABLE IF NOT EXISTS content_skills (
    id TEXT PRIMARY KEY,
    content_id TEXT NOT NULL,
    skill_id TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_content_skills_content ON content_skills(content_id);
CREATE INDEX IF NOT EXISTS ix_content_skills_skill ON content_skills(skill_id);
"""

MIGRATE_POSTS_TO_CONTENT_PG = """
INSERT INTO content (id, community_id, type, title, body, created_at)
SELECT p.id, p.community_id, 'post', p.title, p.body, p.created_at
FROM posts p
ON CONFLICT (id) DO NOTHING;
"""

MIGRATE_EVENTS_TO_CONTENT_PG = """
INSERT INTO content (id, community_id, type, title, event_date, city, location, description, registration, format, media_id, created_at)
SELECT e.id, e.community_id, 'event', e.title, e.starts_at, e.city, e.location, e.description, e.registration, e.format, e.media_id, NOW()
FROM events e
ON CONFLICT (id) DO NOTHING;
"""

MIGRATE_POST_MEDIA_TO_CONTENT_MEDIA_PG = """
INSERT INTO content_media (id, content_id, media_id, order_index)
SELECT pm.id, pm.post_id, pm.media_id, pm.order_index
FROM post_media pm
ON CONFLICT (id) DO NOTHING;
"""

MIGRATE_POSTS_TO_CONTENT_SQLITE = """
INSERT OR IGNORE INTO content (id, community_id, type, title, body, created_at)
SELECT p.id, p.community_id, 'post', p.title, p.body, p.created_at
FROM posts p;
"""

MIGRATE_EVENTS_TO_CONTENT_SQLITE = """
INSERT OR IGNORE INTO content (id, community_id, type, title, event_date, city, location, description, registration, format, media_id, created_at)
SELECT e.id, e.community_id, 'event', e.title, e.starts_at, e.city, e.location, e.description, e.registration, e.format, e.media_id, datetime('now')
FROM events e;
"""

MIGRATE_POST_MEDIA_TO_CONTENT_MEDIA_SQLITE = """
INSERT OR IGNORE INTO content_media (id, content_id, media_id, order_index)
SELECT pm.id, pm.post_id, pm.media_id, pm.order_index
FROM post_media pm;
"""

ALTER_EVENT_PARTICIPANTS_TO_CONTENT_PG = """
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name='event_participants' AND column_name='event_id'
    ) THEN
        -- Drop old constraint if exists
        BEGIN
            ALTER TABLE event_participants DROP CONSTRAINT IF EXISTS event_participants_event_id_fkey;
        EXCEPTION WHEN undefined_object THEN NULL; END;
        -- Rename column
        ALTER TABLE event_participants RENAME COLUMN event_id TO content_id;
    END IF;
    -- Ensure FK to content
    BEGIN
        ALTER TABLE event_participants
        ADD CONSTRAINT event_participants_content_id_fkey FOREIGN KEY (content_id) REFERENCES content(id);
    EXCEPTION WHEN duplicate_object THEN NULL; END;
END$$;
"""

ALTER_EVENT_PARTICIPANTS_TO_CONTENT_SQLITE = """
-- SQLite lacks easy ALTER support; best-effort: leave as-is.
-- Consumers will use content_id column if present; script does not enforce in SQLite.
"""


async def main():
    async with engine.begin() as conn:
        dialect = conn.dialect.name
        if dialect.startswith("postgres"):
            await conn.execute(text(CREATE_CONTENT_PG))
            await conn.execute(text(CREATE_CONTENT_MEDIA_PG))
            await conn.execute(text(CREATE_CONTENT_SKILLS_PG))
            await conn.execute(text(MIGRATE_POSTS_TO_CONTENT_PG))
            await conn.execute(text(MIGRATE_EVENTS_TO_CONTENT_PG))
            await conn.execute(text(MIGRATE_POST_MEDIA_TO_CONTENT_MEDIA_PG))
            await conn.execute(text(ALTER_EVENT_PARTICIPANTS_TO_CONTENT_PG))
            print("Unified content migration completed (Postgres)")
        else:
            await conn.execute(text(CREATE_CONTENT_SQLITE))
            await conn.execute(text(CREATE_CONTENT_MEDIA_SQLITE))
            await conn.execute(text(CREATE_CONTENT_SKILLS_SQLITE))
            await conn.execute(text(MIGRATE_POSTS_TO_CONTENT_SQLITE))
            await conn.execute(text(MIGRATE_EVENTS_TO_CONTENT_SQLITE))
            await conn.execute(text(MIGRATE_POST_MEDIA_TO_CONTENT_MEDIA_SQLITE))
            await conn.execute(text(ALTER_EVENT_PARTICIPANTS_TO_CONTENT_SQLITE))
            print("Unified content migration completed (SQLite)")


if __name__ == "__main__":
    asyncio.run(main())

