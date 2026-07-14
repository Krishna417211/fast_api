from dataclasses import dataclass


@dataclass
class Venue:
    id: int
    name: str
    capacity: int
    location: str | None
