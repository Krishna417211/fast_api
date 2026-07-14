"""Application factory and router wiring."""
import logging

from fastapi import Depends, FastAPI

from .config import get_settings
from .dependencies import get_query_token, get_token_header
from .exceptions import register_exception_handlers
from .internal import admin
from .middleware import LoggingMiddleware, TimingMiddleware
from .routers import (
    announcements,
    attendees,
    events,
    sessions,
    speakers,
    tickets,
    venues,
)

logging.basicConfig(level=logging.INFO)


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version=settings.version)

    # Middleware
    app.add_middleware(TimingMiddleware)
    app.add_middleware(LoggingMiddleware)

    # Exception handlers
    register_exception_handlers(app)

    # Public routers
    app.include_router(events.router)
    app.include_router(venues.router)
    app.include_router(speakers.router)
    app.include_router(sessions.router)
    app.include_router(attendees.router)
    app.include_router(tickets.router)
    app.include_router(announcements.router)

    # Internal admin router, mounted with placeholder token deps (demo, not real auth)
    app.include_router(
        admin.router,
        prefix="/admin",
        tags=["admin"],
        dependencies=[Depends(get_token_header), Depends(get_query_token)],
        responses={418: {"description": "I'm a teapot"}},
    )

    @app.get("/", tags=["root"])
    def root() -> dict:
        return {"app": settings.app_name, "version": settings.version, "docs": "/docs"}

    return app


app = create_app()
