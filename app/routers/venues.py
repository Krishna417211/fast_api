from typing import Annotated

from fastapi import APIRouter, Depends, status

from ..database import Database, get_db
from ..dependencies import Pagination
from ..schemas.venue import VenueCreate, VenueRead, VenueUpdate
from ..services import VenueService

router = APIRouter(
    prefix="/venues",
    tags=["venues"],
    responses={404: {"description": "Venue not found"}},
)


def get_service(db: Annotated[Database, Depends(get_db)]) -> VenueService:
    return VenueService(db)


@router.post("", response_model=VenueRead, status_code=status.HTTP_201_CREATED)
def create_venue(payload: VenueCreate, svc: Annotated[VenueService, Depends(get_service)]):
    return svc.create(payload)


@router.get("", response_model=list[VenueRead])
def list_venues(
    svc: Annotated[VenueService, Depends(get_service)],
    page: Annotated[Pagination, Depends()],
):
    return page.paginate(svc.list())


@router.get("/{venue_id}", response_model=VenueRead)
def get_venue(venue_id: int, svc: Annotated[VenueService, Depends(get_service)]):
    return svc.get(venue_id)


@router.patch("/{venue_id}", response_model=VenueRead)
def update_venue(
    venue_id: int,
    payload: VenueUpdate,
    svc: Annotated[VenueService, Depends(get_service)],
):
    return svc.update(venue_id, payload)


@router.delete("/{venue_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_venue(venue_id: int, svc: Annotated[VenueService, Depends(get_service)]):
    svc.delete(venue_id)
