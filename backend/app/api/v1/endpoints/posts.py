from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.models import User, Post, Like
from app.models.notification import SeverityLevel as ContentSeverity
from app.schemas.post import PostCreate, PostResponse, PostUpdate
from app.services.ai_moderation import ai_moderator
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=PostResponse)
async def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Post:
    """
    Create a new post with AI content moderation
    """
    # Analyze content using AI moderation
    moderation_result = await ai_moderator.analyze_content(post.content)

    # Create post with moderation results
    db_post = Post(
        content=post.content,
        user_id=current_user.id,
        is_moderated=True,
        is_negative=moderation_result["is_negative"],
        moderation_severity=moderation_result["severity"],
        moderation_reason=moderation_result["reason"],
        is_hidden=moderation_result["severity"] in [ContentSeverity.MEDIUM, ContentSeverity.HIGH]
    )

    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    # If content is highly negative, notify admins (implement notification system)
    if moderation_result["severity"] == ContentSeverity.HIGH:
        # TODO: Implement admin notification system
        pass

    return db_post

@router.get("/", response_model=List[PostResponse])
def get_posts(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(deps.get_current_user)
) -> List[Post]:
    """
    Retrieve posts with moderation status
    """
    # Get posts that aren't hidden or are owned by the current user
    posts = db.query(Post).filter(
        (Post.is_hidden == False) | (Post.user_id == current_user.id)
    ).order_by(Post.created_at.desc()).offset(skip).limit(limit).all()

    return posts

@router.get("/{post_id}", response_model=PostResponse)
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(deps.get_current_user)
) -> Post:
    """
    Get a specific post by ID
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Check if post is hidden and user is not the author
    if post.is_hidden and post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Post is hidden due to content violation")

    return post

@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_update: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Post:
    """
    Update a post with new AI content moderation
    """
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if db_post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")

    # Re-analyze content using AI moderation
    moderation_result = await ai_moderator.analyze_content(post_update.content)

    # Update post with new content and moderation results
    db_post.content = post_update.content
    db_post.is_moderated = True
    db_post.is_negative = moderation_result["is_negative"]
    db_post.moderation_severity = moderation_result["severity"]
    db_post.moderation_reason = moderation_result["reason"]
    db_post.is_hidden = moderation_result["severity"] in [ContentSeverity.MEDIUM, ContentSeverity.HIGH]

    db.commit()
    db.refresh(db_post)

    return db_post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Delete a post
    """
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if db_post.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")

    db.delete(db_post)
    db.commit()

@router.post("/{post_id}/like", response_model=PostResponse)
def like_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Post:
    """
    Like or unlike a post
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Check if user has already liked the post
    existing_like = db.query(Like).filter(
        Like.post_id == post_id,
        Like.user_id == current_user.id
    ).first()

    if existing_like:
        # Unlike the post
        db.delete(existing_like)
    else:
        # Like the post
        like = Like(post_id=post_id, user_id=current_user.id)
        db.add(like)

    db.commit()
    db.refresh(post)
    return post 