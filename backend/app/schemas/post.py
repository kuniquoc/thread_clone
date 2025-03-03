from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.models.notification import SeverityLevel as ContentSeverity

class PostBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=500)

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: datetime
    
    # Moderation fields
    is_moderated: bool
    is_negative: bool
    moderation_severity: Optional[ContentSeverity]
    moderation_reason: Optional[str]
    is_hidden: bool
    
    # Stats
    like_count: int = 0
    comment_count: int = 0

    class Config:
        from_attributes = True

class PostWithWarning(PostResponse):
    warning_message: Optional[str] = None

    @classmethod
    def from_post(cls, post: PostResponse) -> "PostWithWarning":
        warning = None
        if post.is_negative:
            if post.moderation_severity == ContentSeverity.LOW:
                warning = "This post may contain inappropriate content"
            elif post.moderation_severity == ContentSeverity.MEDIUM:
                warning = "This post contains potentially offensive content"
            elif post.moderation_severity == ContentSeverity.HIGH:
                warning = "This post has been hidden due to violation of community guidelines"
        
        return cls(
            **post.dict(),
            warning_message=warning
        ) 