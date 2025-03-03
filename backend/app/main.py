from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routes import users, posts, auth, comments
import uvicorn

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Threads Clone API",
    description="A FastAPI backend for a Threads clone with AI content moderation",
    version="1.0.0"
)

# Configure CORS
origins = [
    "http://localhost:3000",  # React development server
    "http://localhost:5173",  # Vite development server
    "https://your-production-frontend-domain.com"  # Add your production domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(comments.router, prefix="/comments", tags=["Comments"])

@app.get("/")
async def root():
    """Root endpoint to check if API is running."""
    return {
        "message": "Welcome to Threads Clone API",
        "status": "running",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
