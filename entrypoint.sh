#!/bin/sh
set -e

# Default DB host for local Docker Compose; override in AWS with the RDS endpoint
DB_HOST="${DB_HOST:-db}"
DB_USER="${DB_USER:-scout}"
DB_NAME="${DB_NAME:-scout}"

echo "Waiting for database at $DB_HOST..."
until pg_isready -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME"; do
  sleep 2
done
echo "Database is ready."

echo "Running migrations..."
alembic upgrade head

echo "Seeding sources (idempotent)..."
python -m scripts.seed_sources || echo "Seed skipped or failed (non-fatal)"

echo "Starting API..."
# No --reload in production
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
