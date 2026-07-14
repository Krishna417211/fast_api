from __future__ import annotations

from ..database import Database
from ..exceptions import NotFoundError
from ..schemas.venue import VenueCreate, VenueUpdate


class VenueService:
    def __init__(self, db: Database) -> None:
        self.table = db.venues

    def create(self, data: VenueCreate) -> dict:
        return self.table.insert(data.model_dump(mode="json"))

    def list(self) -> list[dict]:
        return self.table.list()

    def get(self, venue_id: int) -> dict:
        row = self.table.get(venue_id)
        if row is None:
            raise NotFoundError("Venue", venue_id)
        return row

    def update(self, venue_id: int, data: VenueUpdate) -> dict:
        self.get(venue_id)
        return self.table.update(venue_id, data.model_dump(mode="json", exclude_unset=True))

    def delete(self, venue_id: int) -> None:
        self.get(venue_id)
        self.table.delete(venue_id)
