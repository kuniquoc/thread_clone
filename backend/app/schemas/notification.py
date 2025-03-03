from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.notification import NotificationType, ContentType, SeverityLevel

class NotificationBase(BaseModel):
    type: NotificationType
    severity: SeverityLevel
    content: str
    content_id: int
    content_type: ContentType

class NotificationCreate(NotificationBase):
    pass

class NotificationResponse(NotificationBase):
    id: int
    created_at: datetime
    is_read: bool

    class Config:
        from_attributes = True 