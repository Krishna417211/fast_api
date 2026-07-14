from __future__ import annotations

from ..database import Database
from ..exceptions import NotFoundError
from ..schemas.event import EventCreate, EventUpdate


class EventService:
    def __init__(self, db: Database) -> None:
        self.table = db.events

    def create(self, data: EventCreate) -> dict:
        return self.table.insert(data.model_dump(mode="json"))

    def list(self) -> list[dict]:
        return self.table.list()

    def get(self, event_id: int) -> dict:
        row = self.table.get(event_id)
        if row is None:
            raise NotFoundError("Event", event_id)
        return row

    def update(self, event_id: int, data: EventUpdate) -> dict:
        self.get(event_id)
        return self.table.update(event_id, data.model_dump(mode="json", exclude_unset=True))

    def delete(self, event_id: int) -> None:
        self.get(event_id)
        self.table.delete(event_id)
