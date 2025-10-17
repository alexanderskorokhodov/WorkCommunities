import uvicorn
from fastapi import FastAPI

from app.adapters.db import engine
from app.infrastructure.repos.sql_models import Base
from app.presentation.api.router import api

app = FastAPI(title="Communities API")
app.include_router(api)


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
