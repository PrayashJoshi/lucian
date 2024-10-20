from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..services.orchestrator import Orchestrator

router = APIRouter()
orchestrator = Orchestrator()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print("Client connected.")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print("Client disconnected.")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await manager.connect(websocket)
        while True:
            data = await websocket.receive_text()
            print(f"Received message from frontend: {data}")

            # Get the response from the orchestrator
            response = await orchestrator.process_user_message(data)
            print(f"Sending response to frontend: {response}")

            await manager.send_personal_message(response, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
