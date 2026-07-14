from __future__ import annotations

from ..database import Database
from ..exceptions import ConflictError, NotFoundError
from ..schemas.session import SessionCreate, SessionUpdate


class SessionService:
    def __init__(self, db: Database) -> None:
        self.db = db
        self.table = db.sessions

    def _validate_refs(self, event_id: int, speaker_id: int, venue_id: int) -> None:
        if self.db.events.get(event_id) is None:
            raise NotFoundError("Event", event_id)
        if self.db.speakers.get(speaker_id) is None:
            raise NotFoundError("Speaker", speaker_id)
        if self.db.venues.get(venue_id) is None:
            raise NotFoundError("Venue", venue_id)

    def create(self, data: SessionCreate) -> dict:
        self._validate_refs(data.event_id, data.speaker_id, data.venue_id)
        if data.ends_at <= data.starts_at:
            raise ConflictError("Session end time must be after start time")
        return self.table.insert(data.model_dump(mode="json"))

    def list(self) -> list[dict]:
        return self.table.list()

    def list_for_event(self, event_id: int) -> list[dict]:
        return [s for s in self.table.list() if s["event_id"] == event_id]

    def get(self, session_id: int) -> dict:
        row = self.table.get(session_id)
        if row is None:
            raise NotFoundError("Session", session_id)
        return row

    def update(self, session_id: int, data: SessionUpdate) -> dict:
        self.get(session_id)
        return self.table.update(session_id, data.model_dump(mode="json", exclude_unset=True))

    def delete(self, session_id: int) -> None:
        self.get(session_id)
        self.table.delete(session_id)
