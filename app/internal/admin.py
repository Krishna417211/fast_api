"""Internal admin/reporting endpoints.

Mounted with placeholder token dependencies (demo only, not real auth).
"""
from typing import Annotated

from fastapi import APIRouter, Depends

from ..database import Database, get_db

router = APIRouter()


@router.get("/stats")
def stats(db: Annotated[Database, Depends(get_db)]) -> dict:
    return {
        "events": len(db.events.list()),
        "venues": len(db.venues.list()),
        "speakers": len(db.speakers.list()),
        "sessions": len(db.sessions.list()),
        "attendees": len(db.attendees.list()),
        "tickets": len(db.tickets.list()),
        "checked_in": sum(1 for t in db.tickets.list() if t["checked_in"]),
    }


@router.get("/events/{event_id}/report")
def event_report(event_id: int, db: Annotated[Database, Depends(get_db)]) -> dict:
    sessions = [s for s in db.sessions.list() if s["event_id"] == event_id]
    attendees = [a for a in db.attendees.list() if a["event_id"] == event_id]
    session_ids = {s["id"] for s in sessions}
    tickets = [t for t in db.tickets.list() if t["session_id"] in session_ids]
    return {
        "event_id": event_id,
        "session_count": len(sessions),
        "attendee_count": len(attendees),
        "ticket_count": len(tickets),
        "checked_in": sum(1 for t in tickets if t["checked_in"]),
    }
