from dataclasses import dataclass
from datetime import date


@dataclass
class Event:
    id: int
    name: str
    description: str | None
    start_date: date
    end_date: date
