from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.db.database import engine
from app.db.base import Base
from app.api.v1 import auth, company, email_config, signature, preferences, agent, emails


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


settings = get_settings()

app = FastAPI(
    title="Email Agent API",
    description="Profile & Email Configuration Module",
    version="1.0.0",
    lifespan=lifespan,
)

origins = [origin.strip() for origin in settings.ALLOWED_ORIGINS.split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(company.router, prefix="/api/v1")
app.include_router(email_config.router, prefix="/api/v1")
app.include_router(signature.router, prefix="/api/v1")
app.include_router(preferences.router, prefix="/api/v1")
app.include_router(agent.router, prefix="/api/v1")
app.include_router(emails.router, prefix="/api/v1")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred"},
    )


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
