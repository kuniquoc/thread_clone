from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.models import User, Comment, Post, Like
from app.models.notification import SeverityLevel as ContentSeverity
from app.schemas.comment import CommentCreate, CommentResponse, CommentUpdate
from app.services.ai_moderation import ai_moderator
from app.db.session import get_db

router = APIRouter()

@router.post("/{post_id}", response_model=CommentResponse)
async def create_comment(
    post_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Create new comment with AI content moderation
    """
    # Check if post exists
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Analyze content using AI moderation
    moderation_result = await ai_moderator.analyze_content(comment.content)

    # Create comment with moderation results
    db_comment = Comment(
        content=comment.content,
        user_id=current_user.id,
        post_id=post_id,
        parent_id=comment.parent_id,
        is_moderated=True,
        is_negative=moderation_result["is_negative"],
        moderation_severity=moderation_result["severity"],
        moderation_reason=moderation_result["reason"],
        is_hidden=moderation_result["severity"] in [ContentSeverity.MEDIUM, ContentSeverity.HIGH]
    )

    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)

    return db_comment

@router.get("/post/{post_id}", response_model=List[CommentResponse])
def get_comments(
    post_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Get all comments for a post
    """
    comments = db.query(Comment).filter(
        Comment.post_id == post_id,
        (Comment.is_hidden == False) | (Comment.user_id == current_user.id)
    ).offset(skip).limit(limit).all()
    
    return comments

@router.get("/{comment_id}", response_model=CommentResponse)
def get_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Get a specific comment
    """
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.is_hidden and comment.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Comment is hidden due to content violation"
        )

    return comment

@router.put("/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: int,
    comment_update: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Update a comment with new AI content moderation
    """
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if db_comment.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to update this comment"
        )

    # Re-analyze content using AI moderation
    moderation_result = await ai_moderator.analyze_content(comment_update.content)

    # Update comment with new content and moderation results
    db_comment.content = comment_update.content
    db_comment.is_moderated = True
    db_comment.is_negative = moderation_result["is_negative"]
    db_comment.moderation_severity = moderation_result["severity"]
    db_comment.moderation_reason = moderation_result["reason"]
    db_comment.is_hidden = moderation_result["severity"] in [ContentSeverity.MEDIUM, ContentSeverity.HIGH]

    db.commit()
    db.refresh(db_comment)

    return db_comment

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Delete a comment
    """
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if db_comment.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to delete this comment"
        )

    db.delete(db_comment)
    db.commit()

@router.post("/{comment_id}/like", response_model=CommentResponse)
def like_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Like or unlike a comment
    """
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    # Check if user has already liked the comment
    existing_like = db.query(Like).filter(
        Like.comment_id == comment_id,
        Like.user_id == current_user.id
    ).first()

    if existing_like:
        # Unlike the comment
        db.delete(existing_like)
    else:
        # Like the comment
        like = Like(comment_id=comment_id, user_id=current_user.id)
        db.add(like)

    db.commit()
    db.refresh(comment)
    return comment 