#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

compose_file="$ROOT_DIR/docker-compose.yml"

# Ensure images exist
if ! docker image inspect resumax-api:latest >/dev/null 2>&1 || ! docker image inspect resumax-frontend:latest >/dev/null 2>&1; then
  echo "Images resumax-api:latest or resumax-frontend:latest not found. Run 'make docker-build' first." >&2
  exit 1
fi

trap "docker compose -f '$compose_file' down" EXIT
docker compose -f "$compose_file" up
