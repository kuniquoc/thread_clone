from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any
from ..database import get_db
from ..models import User, Post
from ..schemas import UserResponse, UserUpdate
from ..core.security import get_current_user

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get current user's profile."""
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_current_user_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Update current user's profile."""
    # Check if email is taken
    if user_update.email:
        db_user = db.query(User)\
            .filter(User.email == user_update.email)\
            .filter(User.id != current_user.id)\
            .first()
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Update user
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(current_user, key, value)
    
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/{username}", response_model=UserResponse)
async def get_user_profile(
    username: str,
    db: Session = Depends(get_db)
) -> Any:
    """Get a user's profile by username."""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.get("/{username}/posts", response_model=List[Post])
async def get_user_posts(
    username: str,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
) -> Any:
    """Get all posts by a specific user."""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    posts = db.query(Post)\
        .filter(Post.author_id == user.id)\
        .offset(skip)\
        .limit(limit)\
        .all()
    return posts 