from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.websockets import WebSocketDisconnect, WebSocket
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session, async_session_maker
from .models import Message

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/chat")


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, add_to_db: bool):
        if add_to_db:
            await self.add_messages_to_db(message)
        for connection in self.active_connections:
            await connection.send_text(message)

    @staticmethod
    async def add_messages_to_db(message: str):
        async with async_session_maker() as session:
            query = insert(Message).values(message=message)
            await session.execute(query)
            await session.commit()


manager = ConnectionManager()


@router.get("/")
async def get_chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client #{client_id} says: {data}", add_to_db=True)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat", add_to_db=False)