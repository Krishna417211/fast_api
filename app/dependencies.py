"""Shared dependencies: pagination and placeholder token checks.

The token functions below are NOT authentication. They mirror the FastAPI
"Bigger Applications" tutorial's fake-token dependencies to demonstrate how to
attach router-level / app-level dependencies. Delete them freely.
"""
from typing import Annotated

from fastapi import Header, HTTPException, Query

from .config import get_settings

settings = get_settings()


async def get_token_header(x_token: Annotated[str | None, Header()] = None) -> None:
    """Placeholder header check (demo only, not real auth)."""
    if x_token is not None and x_token != settings.fake_header_token:
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str | None = None) -> None:
    """Placeholder query-param check (demo only, not real auth)."""
    if token is not None and token != settings.fake_query_token:
        raise HTTPException(status_code=400, detail="No jessica token provided")


class Pagination:
    """Reusable pagination dependency."""

    def __init__(
        self,
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=settings.max_page_size)] = settings.default_page_size,
    ) -> None:
        self.skip = skip
        self.limit = limit

    def paginate(self, items: list) -> list:
        return items[self.skip : self.skip + self.limit]
