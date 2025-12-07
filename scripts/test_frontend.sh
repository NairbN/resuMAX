#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FE_DIR="$ROOT_DIR/apps/frontend"

cd "$FE_DIR"
echo "[frontend] Running unit/integration tests..."
pnpm vitest run

echo "[frontend] Skipping e2e tests (disabled per request)."
