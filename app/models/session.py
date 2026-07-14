from dataclasses import dataclass
from datetime import datetime


@dataclass
class Session:
    id: int
    title: str
    event_id: int
    speaker_id: int
    venue_id: int
    starts_at: datetime
    ends_at: datetime
