from typing import Annotated

from fastapi import APIRouter, Depends, status

from ..database import Database, get_db
from ..dependencies import Pagination
from ..schemas.event import EventCreate, EventRead, EventUpdate
from ..schemas.session import SessionRead
from ..services import EventService, SessionService

router = APIRouter(
    prefix="/events",
    tags=["events"],
    responses={404: {"description": "Event not found"}},
)


def get_service(db: Annotated[Database, Depends(get_db)]) -> EventService:
    return EventService(db)


@router.post("", response_model=EventRead, status_code=status.HTTP_201_CREATED)
def create_event(payload: EventCreate, svc: Annotated[EventService, Depends(get_service)]):
    return svc.create(payload)


@router.get("", response_model=list[EventRead])
def list_events(
    svc: Annotated[EventService, Depends(get_service)],
    page: Annotated[Pagination, Depends()],
):
    return page.paginate(svc.list())


@router.get("/{event_id}", response_model=EventRead)
def get_event(event_id: int, svc: Annotated[EventService, Depends(get_service)]):
    return svc.get(event_id)


@router.get("/{event_id}/sessions", response_model=list[SessionRead])
def list_event_sessions(event_id: int, db: Annotated[Database, Depends(get_db)]):
    svc = EventService(db)
    svc.get(event_id)  # 404 if missing
    return SessionService(db).list_for_event(event_id)


@router.patch("/{event_id}", response_model=EventRead)
def update_event(
    event_id: int,
    payload: EventUpdate,
    svc: Annotated[EventService, Depends(get_service)],
):
    return svc.update(event_id, payload)


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: int, svc: Annotated[EventService, Depends(get_service)]):
    svc.delete(event_id)
