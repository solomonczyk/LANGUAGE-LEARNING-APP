# Local Runbook

## Prerequisites

- Python 3.12+
- Node.js 20+
- Docker and Docker Compose
- PostgreSQL 16 (or use Docker)

## Quick Start

### 1. Start Database

```bash
docker compose up postgres -d
```

### 2. Run Backend

```bash
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Copy environment
cp .env.example .env

# Run migrations
alembic upgrade head

# Seed data
python -m app.seed

# Start server
uvicorn app.main:app --reload --port 8000
```

### 3. Run Mobile

```bash
cd mobile

# Install dependencies
npm install

# Start Expo
npx expo start
```

### 4. Full Docker Environment

```bash
# Start everything
docker compose up --build

# This starts:
# - PostgreSQL 16 on port 5432
# - Backend on port 8000 (with auto-migration and seed)
```

## Test Commands

### Backend Tests

```bash
cd backend

# All tests
pytest

# Unit tests only
pytest tests/unit -v

# With coverage
pytest --cov=app --cov-report=term

# Specific test file
pytest tests/unit/test_diagnostics.py -v
```

### Mobile Tests

```bash
cd mobile
npm test
```

## Utility Commands

### Reset Local Environment

```bash
# Stop and remove database
docker compose down -v

# Rebuild
docker compose up --build
```

### Check Database

```bash
# Connect to PostgreSQL
docker exec -it llapp-postgres psql -U llapp -d llapp

# List tables
\dt

# Check seed data
SELECT * FROM users;
SELECT * FROM lesson_definitions;
```

### API Health Check

```bash
curl http://localhost:8000/api/v1/health
```
