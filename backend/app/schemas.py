from pydantic import BaseModel, EmailStr, constr
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None
    bio: Optional[str] = None

class UserCreate(UserBase):
    password: constr(min_length=8)

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    email: Optional[EmailStr] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

# Post schemas
class PostBase(BaseModel):
    content: constr(min_length=1, max_length=5000)

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    author_id: int
    author: UserResponse
    like_count: Optional[int] = 0
    comment_count: Optional[int] = 0

    class Config:
        from_attributes = True

# Comment schemas
class CommentBase(BaseModel):
    content: constr(min_length=1, max_length=1000)

class CommentCreate(CommentBase):
    post_id: int

class CommentUpdate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    post_id: int
    author_id: int
    author: UserResponse

    class Config:
        from_attributes = True

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Like schema
class LikeResponse(BaseModel):
    id: int
    post_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
