from pydantic import BaseModel, Field


class VenueBase(BaseModel):
    name: str = Field(..., examples=["Main Hall"])
    capacity: int = Field(..., ge=1)
    location: str | None = None


class VenueCreate(VenueBase):
    pass


class VenueUpdate(BaseModel):
    name: str | None = None
    capacity: int | None = Field(default=None, ge=1)
    location: str | None = None


class VenueRead(VenueBase):
    id: int
