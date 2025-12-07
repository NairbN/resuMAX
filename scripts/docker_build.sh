#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Building API image..."
docker build -f apps/api/Dockerfile -t resumax-api:latest "$ROOT_DIR"

echo "Building frontend image..."
docker build -f apps/frontend/Dockerfile -t resumax-frontend:latest "$ROOT_DIR"

echo "Done."
