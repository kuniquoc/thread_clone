from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    bio = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")
    likes = relationship("Like", back_populates="user")

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    author_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="post", cascade="all, delete-orphan")

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    post_id = Column(Integer, ForeignKey("posts.id"))
    author_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")

class Like(Base):
    __tablename__ = "likes"
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    post = relationship("Post", back_populates="likes")
    user = relationship("User", back_populates="likes")
