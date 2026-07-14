from pydantic import BaseModel, EmailStr, Field


class SpeakerBase(BaseModel):
    name: str = Field(..., examples=["Ada Lovelace"])
    email: EmailStr
    bio: str | None = None


class SpeakerCreate(SpeakerBase):
    pass


class SpeakerUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    bio: str | None = None


class SpeakerRead(SpeakerBase):
    id: int
