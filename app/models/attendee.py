from dataclasses import dataclass


@dataclass
class Attendee:
    id: int
    name: str
    email: str
    event_id: int
