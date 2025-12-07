#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
API_DIR="$ROOT_DIR/apps/api"
VENV="$API_DIR/.venv"

if [ ! -d "$VENV" ]; then
  echo "Creating virtualenv at $VENV ..."
  python3 -m venv "$VENV"
fi
source "$VENV/bin/activate"

cd "$API_DIR"
pytest -q
