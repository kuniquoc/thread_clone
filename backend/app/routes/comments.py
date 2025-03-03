from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any
from ..database import get_db
from ..models import Comment, User, Post
from ..schemas import CommentCreate, CommentResponse, CommentUpdate
from ..core.security import get_current_user
from ..services.content_moderation import content_moderator

router = APIRouter()

@router.post("/", response_model=CommentResponse)
async def create_comment(
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Create a new comment with content moderation."""
    # Check if post exists
    post = db.query(Post).filter(Post.id == comment.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    # Check content with AI moderation
    moderation_result = await content_moderator.check_content(comment.content)
    if not content_moderator.is_content_allowed(moderation_result):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Comment contains inappropriate material"
        )
    
    # Create comment
    db_comment = Comment(
        content=comment.content,
        post_id=comment.post_id,
        author_id=current_user.id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.get("/post/{post_id}", response_model=List[CommentResponse])
async def get_comments_by_post(
    post_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
) -> Any:
    """Get all comments for a specific post."""
    comments = db.query(Comment)\
        .filter(Comment.post_id == post_id)\
        .offset(skip)\
        .limit(limit)\
        .all()
    return comments

@router.put("/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: int,
    comment_update: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Update a comment."""
    # Get existing comment
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not db_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    
    # Check ownership
    if db_comment.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this comment"
        )
    
    # Check content with AI moderation
    moderation_result = await content_moderator.check_content(comment_update.content)
    if not content_moderator.is_content_allowed(moderation_result):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Comment contains inappropriate material"
        )
    
    # Update comment
    db_comment.content = comment_update.content
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> None:
    """Delete a comment."""
    # Get existing comment
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not db_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    
    # Check ownership
    if db_comment.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this comment"
        )
    
    # Delete comment
    db.delete(db_comment)
    db.commit() 