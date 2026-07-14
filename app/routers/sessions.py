from typing import Annotated

from fastapi import APIRouter, Depends, status

from ..database import Database, get_db
from ..dependencies import Pagination
from ..schemas.session import SessionCreate, SessionRead, SessionUpdate
from ..services import SessionService

router = APIRouter(
    prefix="/sessions",
    tags=["sessions"],
    responses={404: {"description": "Session not found"}},
)


def get_service(db: Annotated[Database, Depends(get_db)]) -> SessionService:
    return SessionService(db)


@router.post("", response_model=SessionRead, status_code=status.HTTP_201_CREATED)
def create_session(payload: SessionCreate, svc: Annotated[SessionService, Depends(get_service)]):
    return svc.create(payload)


@router.get("", response_model=list[SessionRead])
def list_sessions(
    svc: Annotated[SessionService, Depends(get_service)],
    page: Annotated[Pagination, Depends()],
):
    return page.paginate(svc.list())


@router.get("/{session_id}", response_model=SessionRead)
def get_session(session_id: int, svc: Annotated[SessionService, Depends(get_service)]):
    return svc.get(session_id)


@router.patch("/{session_id}", response_model=SessionRead)
def update_session(
    session_id: int,
    payload: SessionUpdate,
    svc: Annotated[SessionService, Depends(get_service)],
):
    return svc.update(session_id, payload)


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(session_id: int, svc: Annotated[SessionService, Depends(get_service)]):
    svc.delete(session_id)
