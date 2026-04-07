"""WebSocket manager for real-time communication"""

from typing import Dict, Set
from fastapi import WebSocket
import asyncio
from backend.core.logger import get_logger

logger = get_logger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.project_connections: Dict[str, Set[str]] = {}
    
    async def connect(self, websocket: WebSocket, project_id: str, client_id: str = None):
        await websocket.accept()
        if client_id is None:
            import uuid
            client_id = str(uuid.uuid4())
        
        self.active_connections[client_id] = websocket
        
        if project_id not in self.project_connections:
            self.project_connections[project_id] = set()
        self.project_connections[project_id].add(client_id)
        
        logger.info(f"Client {client_id} connected to project {project_id}")
        return client_id
    
    def disconnect(self, client_id: str, project_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        if project_id in self.project_connections:
            self.project_connections[project_id].discard(client_id)
        logger.info(f"Client {client_id} disconnected")
    
    async def send_to_project(self, project_id: str, message: dict):
        if project_id not in self.project_connections:
            return
        
        for client_id in self.project_connections[project_id]:
            if client_id in self.active_connections:
                try:
                    await self.active_connections[client_id].send_json(message)
                except Exception as e:
                    logger.error(f"Failed to send to {client_id}: {e}")
    
    async def broadcast(self, message: dict):
        for client_id, websocket in self.active_connections.items():
            try:
                await websocket.send_json(message)
            except Exception as e:
                logger.error(f"Broadcast failed to {client_id}: {e}")

manager = ConnectionManager()