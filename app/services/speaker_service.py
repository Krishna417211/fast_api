from __future__ import annotations

from ..database import Database
from ..exceptions import NotFoundError
from ..schemas.speaker import SpeakerCreate, SpeakerUpdate


class SpeakerService:
    def __init__(self, db: Database) -> None:
        self.table = db.speakers

    def create(self, data: SpeakerCreate) -> dict:
        return self.table.insert(data.model_dump(mode="json"))

    def list(self) -> list[dict]:
        return self.table.list()

    def get(self, speaker_id: int) -> dict:
        row = self.table.get(speaker_id)
        if row is None:
            raise NotFoundError("Speaker", speaker_id)
        return row

    def update(self, speaker_id: int, data: SpeakerUpdate) -> dict:
        self.get(speaker_id)
        return self.table.update(speaker_id, data.model_dump(mode="json", exclude_unset=True))

    def delete(self, speaker_id: int) -> None:
        self.get(speaker_id)
        self.table.delete(speaker_id)
