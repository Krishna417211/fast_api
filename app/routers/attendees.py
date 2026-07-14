from typing import Annotated

from fastapi import APIRouter, Depends, status

from ..database import Database, get_db
from ..dependencies import Pagination
from ..schemas.attendee import AttendeeCreate, AttendeeRead, AttendeeUpdate
from ..services import AttendeeService

router = APIRouter(
    prefix="/attendees",
    tags=["attendees"],
    responses={404: {"description": "Attendee not found"}},
)


def get_service(db: Annotated[Database, Depends(get_db)]) -> AttendeeService:
    return AttendeeService(db)


@router.post("", response_model=AttendeeRead, status_code=status.HTTP_201_CREATED)
def register_attendee(payload: AttendeeCreate, svc: Annotated[AttendeeService, Depends(get_service)]):
    return svc.create(payload)


@router.get("", response_model=list[AttendeeRead])
def list_attendees(
    svc: Annotated[AttendeeService, Depends(get_service)],
    page: Annotated[Pagination, Depends()],
):
    return page.paginate(svc.list())


@router.get("/{attendee_id}", response_model=AttendeeRead)
def get_attendee(attendee_id: int, svc: Annotated[AttendeeService, Depends(get_service)]):
    return svc.get(attendee_id)


@router.patch("/{attendee_id}", response_model=AttendeeRead)
def update_attendee(
    attendee_id: int,
    payload: AttendeeUpdate,
    svc: Annotated[AttendeeService, Depends(get_service)],
):
    return svc.update(attendee_id, payload)


@router.delete("/{attendee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attendee(attendee_id: int, svc: Annotated[AttendeeService, Depends(get_service)]):
    svc.delete(attendee_id)
