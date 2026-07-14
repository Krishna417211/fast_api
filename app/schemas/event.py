from datetime import date

from pydantic import BaseModel, Field


class EventBase(BaseModel):
    name: str = Field(..., examples=["PyCon 2026"])
    description: str | None = None
    start_date: date
    end_date: date


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    start_date: date | None = None
    end_date: date | None = None


class EventRead(EventBase):
    id: int
