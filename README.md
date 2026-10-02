# PLUTON

PLUTON Phase 1 starter project.

## Stack
- Python 3.11
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic

## Setup

1. Create virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Create PostgreSQL database
```sql
CREATE DATABASE pluton;
```

4. Copy env
```bash
cp .env.example .env
```

5. Run app
```bash
uvicorn app.main:app --reload
```

6. Open docs
```text
http://localhost:8000/docs
```

## Phase 1 includes
- Users
- Sports
- Leagues
- Seasons
- Teams
- Fixtures
- Predictions
- Analysis results
- Source registry
- Audit support
