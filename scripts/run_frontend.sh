#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FE_DIR="$ROOT_DIR/apps/frontend"
ENV_FILE="$FE_DIR/.env.local"
EXAMPLE_ENV="$FE_DIR/.env.local.example"

# Regenerate .env.local each run
rm -f "$ENV_FILE"
cp "$EXAMPLE_ENV" "$ENV_FILE"

# Toggle mock based on FRONTEND_MOCK (default true when running frontend alone)
MOCK_VALUE="${FRONTEND_MOCK:-true}"
ENV_FILE="$ENV_FILE" MOCK_VALUE="$MOCK_VALUE" python3 - <<'PY'
import os
from pathlib import Path

env_path = Path(os.environ["ENV_FILE"])
mock_value = os.environ["MOCK_VALUE"]
lines = env_path.read_text().splitlines()
new_lines = []
found = False
for line in lines:
    if line.startswith("NEXT_PUBLIC_USE_AUTH_MOCK="):
        new_lines.append(f"NEXT_PUBLIC_USE_AUTH_MOCK={mock_value}")
        found = True
    else:
        new_lines.append(line)
if not found:
    new_lines.append(f"NEXT_PUBLIC_USE_AUTH_MOCK={mock_value}")
env_path.write_text("\n".join(new_lines) + "\n")
PY

cd "$FE_DIR"

echo "[frontend] Starting on http://localhost:3000 ..."
pnpm dev
