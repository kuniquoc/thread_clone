from fastapi import WebSocket, WebSocketDisconnect, Depends, HTTPException
from typing import Dict, List
import json
from app.core.security import verify_token
from app.models.user import User

class ConnectionManager:
    def __init__(self):
        # Store active connections: {user_id: WebSocket}
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        disconnected_users = []
        for user_id, connection in self.active_connections.items():
            try:
                await connection.send_json(message)
            except WebSocketDisconnect:
                disconnected_users.append(user_id)
        
        # Clean up disconnected users
        for user_id in disconnected_users:
            self.disconnect(user_id)

    async def send_personal_message(self, message: dict, user_id: int):
        """Send message to a specific user"""
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_json(message)
            except WebSocketDisconnect:
                self.disconnect(user_id)

manager = ConnectionManager()

async def get_websocket_user(token: str) -> User:
    """Verify WebSocket connection token"""
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload.get("sub")  # user_id

async def handle_websocket(websocket: WebSocket, token: str):
    """Handle WebSocket connections"""
    try:
        user_id = await get_websocket_user(token)
        await manager.connect(websocket, user_id)
        
        try:
            while True:
                # Wait for messages (if needed for future features)
                data = await websocket.receive_text()
                # Process incoming messages if needed
        except WebSocketDisconnect:
            manager.disconnect(user_id)
    except HTTPException:
        await websocket.close(code=1008)  # Policy Violation

# Notification functions
async def notify_post_created(post_data: dict):
    """Notify all users about new post"""
    await manager.broadcast({
        "type": "post_created",
        "data": post_data
    })

async def notify_post_updated(post_data: dict):
    """Notify all users about post update"""
    await manager.broadcast({
        "type": "post_updated",
        "data": post_data
    })

async def notify_comment_created(comment_data: dict):
    """Notify relevant users about new comment"""
    await manager.broadcast({
        "type": "comment_created",
        "data": comment_data
    })

async def notify_content_moderated(content_data: dict, user_id: int):
    """Notify user about content moderation"""
    await manager.send_personal_message({
        "type": "content_moderated",
        "data": content_data
    }, user_id) 