from typing import Annotated

from fastapi import APIRouter, Depends, status

from ..database import Database, get_db
from ..dependencies import Pagination
from ..schemas.speaker import SpeakerCreate, SpeakerRead, SpeakerUpdate
from ..services import SpeakerService

router = APIRouter(
    prefix="/speakers",
    tags=["speakers"],
    responses={404: {"description": "Speaker not found"}},
)


def get_service(db: Annotated[Database, Depends(get_db)]) -> SpeakerService:
    return SpeakerService(db)


@router.post("", response_model=SpeakerRead, status_code=status.HTTP_201_CREATED)
def create_speaker(payload: SpeakerCreate, svc: Annotated[SpeakerService, Depends(get_service)]):
    return svc.create(payload)


@router.get("", response_model=list[SpeakerRead])
def list_speakers(
    svc: Annotated[SpeakerService, Depends(get_service)],
    page: Annotated[Pagination, Depends()],
):
    return page.paginate(svc.list())


@router.get("/{speaker_id}", response_model=SpeakerRead)
def get_speaker(speaker_id: int, svc: Annotated[SpeakerService, Depends(get_service)]):
    return svc.get(speaker_id)


@router.patch("/{speaker_id}", response_model=SpeakerRead)
def update_speaker(
    speaker_id: int,
    payload: SpeakerUpdate,
    svc: Annotated[SpeakerService, Depends(get_service)],
):
    return svc.update(speaker_id, payload)


@router.delete("/{speaker_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_speaker(speaker_id: int, svc: Annotated[SpeakerService, Depends(get_service)]):
    svc.delete(speaker_id)
