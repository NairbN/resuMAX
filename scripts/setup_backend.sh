#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
API_DIR="$ROOT_DIR/apps/api"
VENV="$API_DIR/.venv"

echo "Setting up backend env..."
cd "$API_DIR"

if [ ! -d "$VENV" ]; then
  echo "Creating virtualenv at $VENV ..."
  python3 -m venv "$VENV"
fi
source "$VENV/bin/activate"

python3 -m pip install --upgrade pip
python3 -m pip install "uvicorn[standard]" alembic sqlalchemy psycopg2-binary redis pytest

echo "Backend setup complete. Activate with: source $VENV/bin/activate"
