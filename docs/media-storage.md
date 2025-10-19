Media storage in Docker

Where files live
- Application saves uploads to `/data/media` inside the `api` container.
- Root `docker-compose.yml` mounts a named volume `media` to persist files across restarts.

Do
- Use `docker compose up -d` from the repository root to ensure the volume is attached.
- Inspect files if needed: `docker compose exec api ls -la /data/media`.
- List volumes: `docker volume ls`; inspect: `docker volume inspect workcommunities_media` (project prefix may vary).

Don’t
- Don’t run `docker compose down -v` on environments where uploads must be preserved — it deletes the `media` volume.

Backup/restore
- Backup: `docker run --rm -v workcommunities_media:/src -v "$PWD":/dst alpine tar -czf /dst/media-backup.tgz -C /src .`
- Restore: `docker run --rm -v workcommunities_media:/dst -v "$PWD":/src alpine sh -c "rm -rf /dst/* && tar -xzf /src/media-backup.tgz -C /dst"`

Re-seeding demo images
- If you rely on mock images, re-run: `docker compose exec api python -m app.scripts.reset_and_seed_demo --base-url http://localhost:8000 --media-dir app/scripts/media_mockups`.
