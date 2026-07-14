from pydantic import BaseModel, Field


class TicketCreate(BaseModel):
    attendee_id: int
    session_id: int
    tier: str = Field(default="standard", examples=["standard", "vip"])


class TicketRead(BaseModel):
    id: int
    attendee_id: int
    session_id: int
    tier: str
    code: str
    checked_in: bool


class CheckInResult(BaseModel):
    ticket_id: int
    checked_in: bool
    message: str
