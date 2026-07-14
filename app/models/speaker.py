from dataclasses import dataclass


@dataclass
class Speaker:
    id: int
    name: str
    email: str
    bio: str | None
