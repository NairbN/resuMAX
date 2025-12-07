#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMPOSE_FILE="$ROOT_DIR/docker-compose.yml"

echo "[dev] Starting dockerized db/redis..."
docker compose -f "$COMPOSE_FILE" up -d db redis

echo "[dev] Starting backend..."
cd "$ROOT_DIR"
DATABASE_URL_OVERRIDE="${DATABASE_URL_OVERRIDE:-postgresql://postgres:postgres@localhost:5432/resumax}" ./scripts/run_api.sh &
BACKEND_PID=$!

echo "[dev] Starting frontend..."
FRONTEND_MOCK=false ./scripts/run_frontend.sh &
FRONTEND_PID=$!

echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo "Press Ctrl+C to stop both."

cleanup() {
  echo "[dev] Stopping..."
  kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
  docker compose -f "$COMPOSE_FILE" down
}

trap cleanup SIGINT SIGTERM

wait
