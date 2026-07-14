from dataclasses import dataclass


@dataclass
class Ticket:
    id: int
    attendee_id: int
    session_id: int
    tier: str
    code: str
    checked_in: bool
