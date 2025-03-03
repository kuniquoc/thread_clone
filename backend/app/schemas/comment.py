from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.models.notification import SeverityLevel as ContentSeverity

class CommentBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=500)
    parent_id: Optional[int] = None

class CommentCreate(CommentBase):
    pass

class CommentUpdate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    user_id: int
    post_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Moderation fields
    is_moderated: bool
    is_negative: bool
    moderation_severity: Optional[ContentSeverity]
    moderation_reason: Optional[str]
    is_hidden: bool
    
    # Stats
    like_count: int = 0
    reply_count: int = 0

    class Config:
        from_attributes = True 