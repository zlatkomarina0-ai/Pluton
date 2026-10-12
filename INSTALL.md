# PLUTON Installation Guide - Phase 3

## Prerequisites
- Python 3.11+
- PostgreSQL 13+
- Node.js 18+ (for frontend)
- Docker & Docker Compose (recommended)

## Quick Start with Docker

```bash
# Clone repository
git clone https://github.com/zlatkomarina0-ai/Pluton.git
cd Pluton

# Copy environment file
cp .env.example .env

# Start services
docker-compose up -d

# Run migrations
docker exec pluton-backend alembic upgrade head

# API documentation
open http://localhost:8000/docs

# Frontend
open http://localhost:3000
```

## Manual Setup

### Backend Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Create database
psql -U postgres -c "CREATE DATABASE pluton_db;"

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
# Frontend runs on http://localhost:3000
```

## Phase 3 Features

- ✅ Sync Engine for real-time data synchronization
- ✅ Frontend integration with Next.js
- ✅ Docker multi-stage builds
- ✅ Type-safe API with TypeScript
- ✅ Comprehensive testing suite

## Troubleshooting

### Database Connection Error
```bash
# Check PostgreSQL is running
psql -U postgres -c "SELECT 1;"

# Verify DATABASE_URL in .env
```

### Port Already in Use
```bash
# Change ports in .env or docker-compose.yml
```

### Frontend Can't Connect to API
```bash
# Ensure NEXT_PUBLIC_API_URL is set correctly in .env
# Backend must be running on port 8000
```

## Support

For issues, check the [STRUCTURE.md](./STRUCTURE.md) or open an issue on GitHub.
