# Scout API
FastAPI + PostgreSQL backend for shared state across Grok scouts and analysts (seen listings, sources, outcodes).

## Quick start (local with Docker)

The easiest way to run everything locally:

```bash
# Optional: copy and edit .env if you want a custom API_KEY
cp .env.example .env

# Build and start both the API and Postgres
docker compose up --build
```

The API will:
- Wait for the database
- Run Alembic migrations
- Seed the three source lists (portals, auctions, receivers)
- Start on http://localhost:8000

Docs: http://localhost:8000/docs  
Health: http://localhost:8000/health

To stop:
```bash
docker compose down
```

To reset the database:
```bash
docker compose down -v
docker compose up --build
```

### Manual (without Docker for the API)
1. `docker compose up -d db`
2. Set `DATABASE_URL=postgresql+asyncpg://scout:scout@localhost:5432/scout` in `.env`
3. `pip install -r requirements.txt`
4. `alembic upgrade head`
5. `python -m scripts.seed_sources`
6. `uvicorn app.main:app --reload --port 8000`

## AWS deployment
See [AWS.md](AWS.md) for the full guide to deploy to App Runner + RDS with automatic deploys from GitHub.