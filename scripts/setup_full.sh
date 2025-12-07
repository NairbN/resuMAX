#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Setting up backend..."
"$ROOT_DIR/scripts/setup_backend.sh"

echo "Setting up frontend..."
"$ROOT_DIR/scripts/setup_frontend.sh"

echo "Setup complete."
