from __future__ import annotations

import secrets

from ..database import Database
from ..exceptions import ConflictError, NotFoundError
from ..schemas.ticket import TicketCreate


class TicketService:
    def __init__(self, db: Database) -> None:
        self.db = db
        self.table = db.tickets

    def issue(self, data: TicketCreate) -> dict:
        if self.db.attendees.get(data.attendee_id) is None:
            raise NotFoundError("Attendee", data.attendee_id)
        if self.db.sessions.get(data.session_id) is None:
            raise NotFoundError("Session", data.session_id)
        payload = data.model_dump(mode="json")
        payload["code"] = secrets.token_urlsafe(8)
        payload["checked_in"] = False
        return self.table.insert(payload)

    def list(self) -> list[dict]:
        return self.table.list()

    def get(self, ticket_id: int) -> dict:
        row = self.table.get(ticket_id)
        if row is None:
            raise NotFoundError("Ticket", ticket_id)
        return row

    def check_in(self, ticket_id: int) -> dict:
        ticket = self.get(ticket_id)
        if ticket["checked_in"]:
            raise ConflictError(f"Ticket {ticket_id} already checked in")
        return self.table.update(ticket_id, {"checked_in": True})
