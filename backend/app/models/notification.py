from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.sql import func
import enum
from app.db.session import Base

class NotificationType(str, enum.Enum):
    moderation = "moderation"
    system = "system"

class ContentType(str, enum.Enum):
    post = "post"
    comment = "comment"

class SeverityLevel(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(NotificationType), nullable=False)
    severity = Column(Enum(SeverityLevel), nullable=False)
    content = Column(String, nullable=False)
    content_id = Column(Integer, nullable=False)
    content_type = Column(Enum(ContentType), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_read = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Notification(id={self.id}, type={self.type}, severity={self.severity})>" 