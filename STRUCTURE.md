# PLUTON Project Structure - Phase 3

## Directory Layout

```
Plution/
├── app/                           # Main application package
│   ├── __init__.py               # Package initialization
│   ├── main.py                   # FastAPI entry point
│   ├── config.py                 # Configuration & settings
│   ├── database.py               # Database connection
│   ├── models.py                 # SQLAlchemy ORM models
│   ├── schemas.py                # Pydantic validation schemas
│   ├── dependencies.py           # FastAPI dependencies
│   ├── core/                     # Core utilities
│   │   └── __init__.py
│   ├── routers/                  # API route handlers
│   │   └── __init__.py
│   ├── services/                 # Business logic
│   │   └── __init__.py
│   ├── book/                     # Booking module
│   │   └── __init__.py
│   ├── phase3/                   # Phase 3: Sync Engine
│   │   ├── __init__.py
│   │   └── sync_engine.py        # Real-time sync implementation
│   └── phase4/                   # Phase 4: Analytics (placeholder)
│       └── __init__.py
├── frontend/                      # Next.js frontend
│   ├── tsconfig.json             # TypeScript configuration
│   ├── next.config.js            # Next.js configuration
│   ├── package.json              # Dependencies
│   ├── src/
│   │   ├── pages/                # Next.js pages
│   │   ├── components/           # React components
│   │   ├── utils/                # Utility functions
│   │   └── types/                # TypeScript type definitions
│   └── public/                   # Static assets
├── backend/                       # Backend utilities
│   └── requirements.txt          # Python dependencies
├── database/                      # Database utilities
├── alembic/                       # Database migrations
│   ├── versions/                 # Migration files
│   └── env.py                    # Alembic configuration
├── tests/                         # Test suite
│   ├── __init__.py
│   └── test_phase3_sync.py       # Sync engine tests
├── Dockerfile                     # Multi-stage Docker build
├── docker-compose.yml             # Docker Compose orchestration
├── .env.example                   # Environment template
├── alembic.ini                    # Alembic config
├── INSTALL.md                     # Installation guide
├── STRUCTURE.md                   # This file
└── README.md                      # Project overview
```

## Component Descriptions

### Backend (FastAPI)
- **main.py**: Application initialization, routes registration
- **models.py**: SQLAlchemy models for Users, Teams, Fixtures, Predictions, etc.
- **schemas.py**: Pydantic models for request/response validation
- **services/**: Business logic layer (separate from routes)
- **routers/**: API endpoint definitions

### Phase 3: Sync Engine
- **sync_engine.py**: Real-time data synchronization between services
- Async queue-based architecture
- Supports entity sync across all domain models

### Frontend (Next.js)
- **tsconfig.json**: Strict TypeScript configuration
- **next.config.js**: API rewrites, image optimization, webpack splitting
- Path aliases for clean imports (@components, @utils, etc.)

### Infrastructure
- **Dockerfile**: Multi-stage build (optimized for production)
- **docker-compose.yml**: PostgreSQL + FastAPI + Redis (optional)
- **.env.example**: All configurable parameters

### Testing
- **tests/**: pytest-based test suite
- Phase 3 sync engine tests included
- Ready for unit and integration tests

## Phase Roadmap

### Phase 1 ✅ (Completed)
- Core models (Users, Teams, Leagues, Seasons, Fixtures, Predictions)
- Basic CRUD operations
- PostgreSQL + SQLAlchemy setup

### Phase 2 (In Progress)
- Advanced API routes
- Authentication & authorization
- Audit logging

### Phase 3 ⚡ (Current - This Deployment)
- Real-time sync engine
- Frontend integration (Next.js)
- Docker optimization
- Comprehensive testing

### Phase 4 (Planned)
- Analytics dashboard
- ML-based predictions
- Advanced reporting

## Key Technologies

| Component | Technology | Version |
|-----------|-----------|----------|
| Backend   | Python    | 3.11+   |
| Framework | FastAPI   | 0.110+  |
| Database  | PostgreSQL| 13+     |
| ORM       | SQLAlchemy| 2.0+    |
| Frontend  | Next.js   | 14+     |
| Language  | TypeScript| 5.0+    |
| Testing   | pytest    | 7.0+    |

## Configuration

All configuration is managed via `.env` file:

```bash
# Copy template
cp .env.example .env

# Edit with your values
vim .env

# Key variables:
DATABASE_URL          # PostgreSQL connection string
NEXT_PUBLIC_API_URL   # Frontend API endpoint
SYNC_ENGINE_ENABLED   # Enable Phase 3 sync
```

## Development Workflow

1. **Start services**: `docker-compose up`
2. **Apply migrations**: `alembic upgrade head`
3. **Run backend**: `uvicorn app.main:app --reload` (port 8000)
4. **Run frontend**: `cd frontend && npm run dev` (port 3000)
5. **API docs**: http://localhost:8000/docs
6. **Frontend**: http://localhost:3000

## Contributing

Follow the phase structure for new features:
- Phase 3: Sync & Frontend features
- Phase 4: Analytics & ML features

Ensure tests pass before merging.
