from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date
from typing import List
from datetime import datetime, timedelta
from app.api import deps
from app.models.notification import Notification, NotificationType, ContentType, SeverityLevel
from app.schemas.notification import NotificationCreate, NotificationResponse
from app.core.security import get_current_admin_user
from app.websocket import notify_content_moderated
from app.core.email import send_moderation_alert

router = APIRouter()

@router.get("/notifications", response_model=List[NotificationResponse])
async def get_notifications(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Get all admin notifications with pagination"""
    notifications = (
        db.query(Notification)
        .order_by(Notification.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return notifications

@router.get("/notifications/unread-count", response_model=dict)
async def get_unread_count(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Get count of unread notifications"""
    count = db.query(Notification).filter(Notification.is_read == False).count()
    return {"count": count}

@router.put("/notifications/{notification_id}/read")
async def mark_as_read(
    notification_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Mark a notification as read"""
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.is_read = True
    db.commit()
    return {"status": "success"}

@router.put("/notifications/read-all")
async def mark_all_as_read(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Mark all notifications as read"""
    db.query(Notification).filter(Notification.is_read == False).update({"is_read": True})
    db.commit()
    return {"status": "success"}

@router.get("/stats")
async def get_moderation_stats(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Get moderation statistics for the analytics dashboard"""
    # Get total violations
    total_violations = db.query(Notification).count()

    # Get violations by severity
    severity_counts = (
        db.query(
            Notification.severity,
            func.count(Notification.id).label('count')
        )
        .group_by(Notification.severity)
        .all()
    )
    violations_by_severity = {
        'low': 0,
        'medium': 0,
        'high': 0
    }
    for severity, count in severity_counts:
        violations_by_severity[severity] = count

    # Get violations by type
    type_counts = (
        db.query(
            Notification.content_type,
            func.count(Notification.id).label('count')
        )
        .group_by(Notification.content_type)
        .all()
    )
    violations_by_type = {
        'post': 0,
        'comment': 0
    }
    for content_type, count in type_counts:
        violations_by_type[content_type] = count

    # Get violations over time (last 7 days)
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    violations_over_time = (
        db.query(
            cast(Notification.created_at, Date).label('date'),
            func.count(Notification.id).label('count')
        )
        .filter(Notification.created_at >= seven_days_ago)
        .group_by(cast(Notification.created_at, Date))
        .order_by(cast(Notification.created_at, Date))
        .all()
    )

    return {
        "total_violations": total_violations,
        "violations_by_severity": violations_by_severity,
        "violations_by_type": violations_by_type,
        "violations_over_time": [
            {"date": date.isoformat(), "count": count}
            for date, count in violations_over_time
        ]
    }

async def create_moderation_notification(
    db: Session,
    content_type: ContentType,
    content_id: int,
    severity: SeverityLevel,
    content: str,
    background_tasks: BackgroundTasks
):
    """Create a new moderation notification with email alert for high severity"""
    notification = Notification(
        type=NotificationType.moderation,
        severity=severity,
        content=content,
        content_id=content_id,
        content_type=content_type
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    
    # Send WebSocket notification
    await notify_content_moderated({
        "id": notification.id,
        "type": notification.type,
        "severity": notification.severity,
        "content": notification.content,
        "contentId": notification.content_id,
        "contentType": notification.content_type,
        "createdAt": notification.created_at.isoformat(),
        "isRead": notification.is_read
    })

    # Send email for high severity violations
    if severity == SeverityLevel.high:
        admin_emails = ["admin@example.com"]  # Replace with actual admin emails
        background_tasks.add_task(
            send_moderation_alert,
            admin_emails=admin_emails,
            content_type=content_type,
            content_id=content_id,
            severity=severity,
            reason=content
        ) 