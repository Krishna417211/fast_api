"""Domain models.

These dataclasses stand in for SQLAlchemy ORM models. When you move to a real
database, replace each with a declarative model — the services layer is the only
place that constructs them, so routers/schemas stay unchanged.
"""
from .event import Event
from .venue import Venue
from .speaker import Speaker
from .session import Session
from .attendee import Attendee
from .ticket import Ticket

__all__ = ["Event", "Venue", "Speaker", "Session", "Attendee", "Ticket"]
