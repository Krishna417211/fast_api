from pydantic import BaseModel, EmailStr, Field


class AttendeeBase(BaseModel):
    name: str = Field(..., examples=["Grace Hopper"])
    email: EmailStr
    event_id: int


class AttendeeCreate(AttendeeBase):
    pass


class AttendeeUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None


class AttendeeRead(AttendeeBase):
    id: int
