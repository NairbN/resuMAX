#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FE_DIR="$ROOT_DIR/apps/frontend"

echo "Setting up frontend dependencies..."
cd "$FE_DIR"
pnpm install
echo "Frontend setup complete."
