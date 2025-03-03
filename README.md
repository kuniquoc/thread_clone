# Threads Clone with AI Content Moderation

A modern social media platform inspired by Threads, featuring AI-powered content moderation to ensure a safe and positive user experience.

## Features

- User authentication and authorization
- Create, read, update, and delete posts
- Comment on posts
- AI-powered content moderation using Hugging Face
- Modern, responsive UI
- Real-time updates
- PostgreSQL database for data persistence

## Tech Stack

### Backend
- FastAPI (Python)
- PostgreSQL
- SQLAlchemy + Alembic
- JWT Authentication
- Hugging Face API for content moderation

### Frontend
- React with TypeScript
- Vite
- Tailwind CSS
- Axios for API calls

## Prerequisites

- Python 3.11+
- Node.js 18+
- Docker and Docker Compose
- Hugging Face API token

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/threads-clone.git
cd threads-clone
```

2. Set up environment variables:
```bash
# Copy example env files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Edit the .env files with your configuration
```

3. Start the development environment:
```bash
# Start all services
docker-compose up -d

# The following services will be available:
# - Backend API: http://localhost:8000
# - Frontend: http://localhost:5173
# - PostgreSQL: localhost:5432
```

4. Initialize the database:
```bash
# Create database tables
docker-compose exec backend alembic upgrade head
```

## Development

### Backend Development

1. Install Python dependencies:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Run migrations:
```bash
alembic upgrade head
```

3. Start the development server:
```bash
uvicorn app.main:app --reload
```

### Frontend Development

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

## Deployment

### Backend Deployment (Render)

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure environment variables
4. Set the build command: `pip install -r requirements.txt`
5. Set the start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Frontend Deployment (Vercel)

1. Push your code to GitHub
2. Import the project in Vercel
3. Configure environment variables
4. Deploy

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
