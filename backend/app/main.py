"""FastAPI application entry point."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text as sa_text

from app.config import settings
from app.database import async_session_factory
from app.shared.middleware.error_handler import add_exception_handlers


app_started = False


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    global app_started
    app_started = True
    yield
    # Shutdown
    app_started = False


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
add_exception_handlers(app)


@app.get("/api/v1/health")
async def health():
    """Health check endpoint — reports live DB connectivity."""
    # Check database connectivity with a simple query
    db_status = "pending"
    try:
        async with async_session_factory() as session:
            await session.execute(sa_text("SELECT 1"))
            db_status = "ready"
    except Exception:
        db_status = "unavailable"

    overall_status = "ok" if db_status == "ready" else "degraded"

    return {
        "status": overall_status,
        "version": "0.1.0",
        "database": db_status,
        "mock_ai": "ready",
    }


# Import and register routers
from app.modules.identity.router import router as identity_router
from app.modules.learner_profile.router import router as learner_profile_router
from app.modules.diagnostics.router import router as diagnostics_router
from app.modules.learning_contract.router import router as learning_contract_router
from app.modules.lesson_engine.router import router as lesson_engine_router
from app.modules.submission.router import router as submission_router
from app.modules.mastery.router import router as mastery_router
from app.modules.audit.router import router as audit_router
from app.modules.operator.router import router as operator_router

app.include_router(identity_router, prefix=settings.api_prefix, tags=["identity"])
app.include_router(learner_profile_router, prefix=settings.api_prefix, tags=["learner-profile"])
app.include_router(diagnostics_router, prefix=settings.api_prefix, tags=["diagnostics"])
app.include_router(learning_contract_router, prefix=settings.api_prefix, tags=["learning-contract"])
app.include_router(lesson_engine_router, prefix=settings.api_prefix, tags=["lesson-engine"])
app.include_router(submission_router, prefix=settings.api_prefix, tags=["submission"])
app.include_router(mastery_router, prefix=settings.api_prefix, tags=["mastery"])
app.include_router(audit_router, prefix=settings.api_prefix, tags=["audit"])
app.include_router(operator_router, prefix=settings.api_prefix, tags=["operator"])
