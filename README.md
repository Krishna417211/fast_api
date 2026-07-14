# Event & Conference Management Platform

A large multi-file FastAPI application (no authentication) built on the
structure of FastAPI's "Bigger Applications" tutorial, scaled up with
models / schemas / services layers, middleware, and a WebSocket router.

## Run

```bash
pip install -r requirements.txt
python run.py          # or: uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs

## Structure

```
app/
├── main.py            # app factory, includes all routers
├── config.py          # settings
├── dependencies.py    # pagination + placeholder token deps (NOT real auth)
├── database.py        # in-memory store (swap for SQLAlchemy later)
├── exceptions.py      # custom exceptions + handlers
├── middleware/        # logging, timing
├── models/            # domain dataclasses (stand-in for ORM models)
├── schemas/           # Pydantic request/response models
├── services/          # business logic, kept out of routers
├── routers/           # events, venues, speakers, sessions,
│                      #   attendees, tickets, announcements (WebSocket)
└── internal/          # admin/reporting endpoints
```

## Notes on "no authentication"

`dependencies.py` includes `get_token_header` / `get_query_token`. These are
**placeholders** copied from the FastAPI tutorial to demonstrate router/app-level
dependencies — they are not authentication. They only reject a token if one is
supplied and it's wrong; omitting the token passes. Delete them to remove entirely.

## Key endpoints

- `POST /events`, `GET /events`, `GET /events/{id}/sessions`
- `POST /venues`, `POST /speakers`
- `POST /sessions` (validates event/speaker/venue references)
- `POST /attendees`, `POST /tickets`, `POST /tickets/{id}/check-in`
- `WS /announcements/ws`, `POST /announcements/broadcast`
- `GET /admin/stats`, `GET /admin/events/{id}/report`
