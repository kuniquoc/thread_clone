from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any
from ..database import get_db
from ..models import Post, User
from ..schemas import PostCreate, PostResponse, PostUpdate
from ..core.security import get_current_user
from ..services.content_moderation import content_moderator

router = APIRouter()

@router.post("/", response_model=PostResponse)
async def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Create a new post with content moderation."""
    # Check content with AI moderation
    moderation_result = await content_moderator.check_content(post.content)
    if not content_moderator.is_content_allowed(moderation_result):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Content contains inappropriate material"
        )
    
    # Create post
    db_post = Post(
        content=post.content,
        author_id=current_user.id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.get("/", response_model=List[PostResponse])
async def get_posts(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
) -> Any:
    """Get all posts with pagination."""
    posts = db.query(Post).offset(skip).limit(limit).all()
    return posts

@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    db: Session = Depends(get_db)
) -> Any:
    """Get a specific post by ID."""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return post

@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_update: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Update a post."""
    # Get existing post
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    # Check ownership
    if db_post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this post"
        )
    
    # Check content with AI moderation
    moderation_result = await content_moderator.check_content(post_update.content)
    if not content_moderator.is_content_allowed(moderation_result):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Content contains inappropriate material"
        )
    
    # Update post
    for key, value in post_update.dict().items():
        setattr(db_post, key, value)
    
    db.commit()
    db.refresh(db_post)
    return db_post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> None:
    """Delete a post."""
    # Get existing post
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    # Check ownership
    if db_post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this post"
        )
    
    # Delete post
    db.delete(db_post)
    db.commit() 