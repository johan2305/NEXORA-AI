import json
import uuid

import redis.asyncio as aioredis
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from backend.core.config import get_settings
from backend.core.database import get_db
from backend.core.dependencies import CurrentUser, get_current_user
from backend.core.security import decode_token
from backend.notifications import repository as notification_repository
from backend.notifications.schemas import NotificationResponse
from backend.notifications.ws_manager import manager

router = APIRouter(prefix="/notifications", tags=["notifications"])

settings = get_settings()

REDIS_URL = settings.redis_url
NOTIFICATIONS_CHANNEL = "nexora:notifications"


@router.get("", response_model=list[NotificationResponse])
def list_notifications(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    return notification_repository.list_all(db, current_user.organization_id)


@router.post("/{notification_id}/read")
def mark_as_read(
    notification_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    notification_repository.mark_as_read(db, current_user.organization_id, notification_id)
    db.commit()
    return {"status": "ok"}


@router.websocket("/ws")
async def notifications_websocket(websocket: WebSocket, token: str):
    payload = decode_token(token)
    if not payload:
        await websocket.close(code=1008)
        return

    organization_id = uuid.UUID(payload["org"])
    await manager.connect(organization_id, websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(organization_id, websocket)


async def redis_listener():
    """
    Corre en segundo plano dentro de FastAPI. Escucha Redis Pub/Sub
    y reenvía cada mensaje al WebSocket de la organización correcta.
    """
    print("🔌 [redis_listener] Iniciando conexión a Redis...")
    try:
        redis_client = aioredis.from_url(REDIS_URL)
        pubsub = redis_client.pubsub()
        await pubsub.subscribe(NOTIFICATIONS_CHANNEL)
        print(f"✅ [redis_listener] Suscrito al canal '{NOTIFICATIONS_CHANNEL}'")

        async for message in pubsub.listen():
            print(f"📨 [redis_listener] Mensaje crudo recibido: {message}")
            if message["type"] != "message":
                continue

            data = json.loads(message["data"])
            print(
                f"📬 [redis_listener] Enviando a organización "
                f"{data['organization_id']}"
            )
            await manager.send_to_organization(
                data["organization_id"],
                data["notification"],
            )
    except Exception as e:
        print(f"❌ [redis_listener] Error: {e}")