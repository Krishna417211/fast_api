from datetime import datetime

from pydantic import BaseModel, Field


class SessionBase(BaseModel):
    title: str = Field(..., examples=["Async Python in Practice"])
    event_id: int
    speaker_id: int
    venue_id: int
    starts_at: datetime
    ends_at: datetime


class SessionCreate(SessionBase):
    pass


class SessionUpdate(BaseModel):
    title: str | None = None
    speaker_id: int | None = None
    venue_id: int | None = None
    starts_at: datetime | None = None
    ends_at: datetime | None = None


class SessionRead(SessionBase):
    id: int
