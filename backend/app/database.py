from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# Get database URL from environment variable or use default for local development
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:admin@localhost/threads")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for database models
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
