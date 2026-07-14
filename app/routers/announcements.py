"""Live announcements over WebSocket, plus an HTTP broadcast trigger."""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

router = APIRouter(prefix="/announcements", tags=["announcements"])


class ConnectionManager:
    def __init__(self) -> None:
        self.active: list[WebSocket] = []

    async def connect(self, ws: WebSocket) -> None:
        await ws.accept()
        self.active.append(ws)

    def disconnect(self, ws: WebSocket) -> None:
        if ws in self.active:
            self.active.remove(ws)

    async def broadcast(self, message: str) -> int:
        for ws in list(self.active):
            await ws.send_json({"announcement": message})
        return len(self.active)


manager = ConnectionManager()


class Announcement(BaseModel):
    message: str


@router.websocket("/ws")
async def announcements_ws(websocket: WebSocket) -> None:
    await manager.connect(websocket)
    try:
        while True:
            # Echo any client message back to everyone.
            data = await websocket.receive_text()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@router.post("/broadcast")
async def broadcast(payload: Announcement) -> dict:
    delivered = await manager.broadcast(payload.message)
    return {"delivered_to": delivered, "message": payload.message}
