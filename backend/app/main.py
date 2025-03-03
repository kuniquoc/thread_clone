from fastapi import FastAPI, WebSocket, Query
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import api_router
from app.db.session import engine, Base
from app.websocket import handle_websocket
import uvicorn

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="""
    🧵 Threads Clone API - A social media platform API built with FastAPI
    
    ## Features
    * 👤 User Authentication
    * 📝 Posts Management
    * 💬 Comments
    * ❤️ Likes
    * 🔔 Real-time Notifications (WebSocket)
    * 🤖 AI Content Moderation
    
    ## Authentication
    * Use the `/auth/login` endpoint to get your access token
    * Click the 'Authorize' button and enter your token as: `Bearer your-token`
    """,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "API Support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
    }
)

# Configure CORS with more permissive settings for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # More permissive for development
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...)
):
    await handle_websocket(websocket, token)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/")
async def root():
    """Root endpoint to check if API is running."""
    return {
        "message": "Welcome to Threads Clone API",
        "status": "running",
        "version": settings.VERSION
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
