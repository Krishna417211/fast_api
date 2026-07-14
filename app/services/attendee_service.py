from __future__ import annotations

from ..database import Database
from ..exceptions import NotFoundError
from ..schemas.attendee import AttendeeCreate, AttendeeUpdate


class AttendeeService:
    def __init__(self, db: Database) -> None:
        self.db = db
        self.table = db.attendees

    def create(self, data: AttendeeCreate) -> dict:
        if self.db.events.get(data.event_id) is None:
            raise NotFoundError("Event", data.event_id)
        return self.table.insert(data.model_dump(mode="json"))

    def list(self) -> list[dict]:
        return self.table.list()

    def get(self, attendee_id: int) -> dict:
        row = self.table.get(attendee_id)
        if row is None:
            raise NotFoundError("Attendee", attendee_id)
        return row

    def update(self, attendee_id: int, data: AttendeeUpdate) -> dict:
        self.get(attendee_id)
        return self.table.update(attendee_id, data.model_dump(mode="json", exclude_unset=True))

    def delete(self, attendee_id: int) -> None:
        self.get(attendee_id)
        self.table.delete(attendee_id)
