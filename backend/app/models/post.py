from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
from app.models.notification import SeverityLevel

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("posts.id"), nullable=True)
    
    # Moderation fields
    is_moderated = Column(Boolean, default=False)
    is_negative = Column(Boolean, default=False)
    moderation_severity = Column(Enum(SeverityLevel), nullable=True)
    moderation_reason = Column(String, nullable=True)
    is_hidden = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    likes = relationship("Like", back_populates="post")
    parent = relationship("Post", remote_side=[id], back_populates="replies")
    replies = relationship("Post", back_populates="parent")

    @property
    def like_count(self) -> int:
        return len(self.likes)

    @property
    def comment_count(self) -> int:
        return len(self.comments) 