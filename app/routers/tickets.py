from typing import Annotated

from fastapi import APIRouter, Depends, status

from ..database import Database, get_db
from ..dependencies import Pagination
from ..schemas.ticket import CheckInResult, TicketCreate, TicketRead
from ..services import TicketService

router = APIRouter(
    prefix="/tickets",
    tags=["tickets"],
    responses={404: {"description": "Ticket not found"}},
)


def get_service(db: Annotated[Database, Depends(get_db)]) -> TicketService:
    return TicketService(db)


@router.post("", response_model=TicketRead, status_code=status.HTTP_201_CREATED)
def issue_ticket(payload: TicketCreate, svc: Annotated[TicketService, Depends(get_service)]):
    return svc.issue(payload)


@router.get("", response_model=list[TicketRead])
def list_tickets(
    svc: Annotated[TicketService, Depends(get_service)],
    page: Annotated[Pagination, Depends()],
):
    return page.paginate(svc.list())


@router.get("/{ticket_id}", response_model=TicketRead)
def get_ticket(ticket_id: int, svc: Annotated[TicketService, Depends(get_service)]):
    return svc.get(ticket_id)


@router.post("/{ticket_id}/check-in", response_model=CheckInResult)
def check_in(ticket_id: int, svc: Annotated[TicketService, Depends(get_service)]):
    ticket = svc.check_in(ticket_id)
    return CheckInResult(
        ticket_id=ticket["id"],
        checked_in=ticket["checked_in"],
        message="Checked in successfully",
    )
