import uuid

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, organization_id: uuid.UUID, websocket: WebSocket):
        await websocket.accept()
        org_key = str(organization_id)
        self.active_connections.setdefault(org_key, []).append(websocket)

    def disconnect(self, organization_id: uuid.UUID, websocket: WebSocket):
        org_key = str(organization_id)
        if org_key in self.active_connections:
            self.active_connections[org_key].remove(websocket)
            if not self.active_connections[org_key]:
                del self.active_connections[org_key]

    async def send_to_organization(self, organization_id: str, message: dict):
        for connection in self.active_connections.get(organization_id, []):
            await connection.send_json(message)


manager = ConnectionManager()