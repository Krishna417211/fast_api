"""Custom exceptions and handlers."""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class NotFoundError(Exception):
    def __init__(self, entity: str, entity_id: int) -> None:
        self.entity = entity
        self.entity_id = entity_id
        super().__init__(f"{entity} with id {entity_id} not found")


class ConflictError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(NotFoundError)
    async def _not_found(request: Request, exc: NotFoundError) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc), "entity": exc.entity, "id": exc.entity_id},
        )

    @app.exception_handler(ConflictError)
    async def _conflict(request: Request, exc: ConflictError) -> JSONResponse:
        return JSONResponse(status_code=409, content={"detail": exc.message})
