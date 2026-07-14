"""In-memory data store.

Swap this module for SQLAlchemy engine/session later without touching routers,
since all data access goes through the services layer.
"""
from __future__ import annotations
from itertools import count
from threading import Lock
from typing import Any


class InMemoryTable:
    """A tiny thread-safe auto-incrementing table."""

    def __init__(self) -> None:
        self._rows: dict[int, dict[str, Any]] = {}
        self._ids = count(1)
        self._lock = Lock()

    def insert(self, data: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            new_id = next(self._ids)
            row = {"id": new_id, **data}
            self._rows[new_id] = row
            return row

    def get(self, row_id: int) -> dict[str, Any] | None:
        return self._rows.get(row_id)

    def list(self) -> list[dict[str, Any]]:
        return list(self._rows.values())

    def update(self, row_id: int, data: dict[str, Any]) -> dict[str, Any] | None:
        with self._lock:
            row = self._rows.get(row_id)
            if row is None:
                return None
            row.update({k: v for k, v in data.items() if v is not None})
            return row

    def delete(self, row_id: int) -> bool:
        with self._lock:
            return self._rows.pop(row_id, None) is not None


class Database:
    """Holds one table per entity."""

    def __init__(self) -> None:
        self.events = InMemoryTable()
        self.venues = InMemoryTable()
        self.speakers = InMemoryTable()
        self.sessions = InMemoryTable()
        self.attendees = InMemoryTable()
        self.tickets = InMemoryTable()


db = Database()


def get_db() -> Database:
    """FastAPI dependency that yields the shared store."""
    return db
