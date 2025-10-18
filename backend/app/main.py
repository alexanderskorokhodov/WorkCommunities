import uvicorn
from fastapi import FastAPI

from app.adapters.db import engine
from app.infrastructure.repos.sql_models import Base
from app.presentation.api.router import api
from app.migrations.auto import run_lightweight_migrations

app = FastAPI(title="Communities API", swagger_ui_parameters={
    "dom_id": "#swagger-ui",
    "layout": "BaseLayout",
    "deepLinking": True,
    "showExtensions": True,
    "showCommonExtensions": True,
})
app.include_router(api)


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Run additive, idempotent migrations to keep old DBs compatible
    await run_lightweight_migrations()


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
