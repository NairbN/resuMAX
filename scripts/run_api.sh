#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
API_DIR="$ROOT_DIR/apps/api"
ENV_FILE="$API_DIR/.env"
EXAMPLE_ENV="$API_DIR/.env.example"
VENV="$API_DIR/.venv"

ensure_venv() {
  if [ ! -d "$VENV" ]; then
    echo "[backend] Creating virtualenv at $VENV ..."
    python3 -m venv "$VENV"
  fi
  # shellcheck disable=SC1090
  source "$VENV/bin/activate"
}

regenerate_env() {
  echo "[backend] Regenerating $ENV_FILE from .env.example..."
  if [ ! -f "$EXAMPLE_ENV" ]; then
    echo "Missing $EXAMPLE_ENV" >&2
    exit 1
  fi
  rm -f "$ENV_FILE"
  cp "$EXAMPLE_ENV" "$ENV_FILE"

  AUTH_SECRET=$(python3 - <<'PY'
import secrets
print(secrets.token_urlsafe(48))
PY
)

  ENV_PATH="$ENV_FILE" AUTH_SECRET_VALUE="$AUTH_SECRET" DATABASE_URL_OVERRIDE="${DATABASE_URL_OVERRIDE:-}" python3 - <<'PY'
import os
from pathlib import Path

env_path = Path(os.environ["ENV_PATH"])
auth_secret = os.environ["AUTH_SECRET_VALUE"]
db_override = os.environ.get("DATABASE_URL_OVERRIDE")

lines = env_path.read_text().splitlines()
new_lines = []
db_written = False
for line in lines:
    if line.startswith("AUTH_SECRET="):
        new_lines.append(f"AUTH_SECRET={auth_secret}")
    elif db_override and line.startswith("DATABASE_URL="):
        new_lines.append(f"DATABASE_URL={db_override}")
        db_written = True
    else:
        new_lines.append(line)

if db_override and not db_written:
    new_lines.append(f"DATABASE_URL={db_override}")

env_path.write_text("\n".join(new_lines) + "\n")
PY
  echo "[backend] Generated AUTH_SECRET."
}

pick_db_url() {
  local db_url="${DATABASE_URL_OVERRIDE:-}"
  if [ -z "$db_url" ]; then
    db_url=$(grep '^DATABASE_URL=' "$ENV_FILE" | head -n1 | cut -d'=' -f2-)
  fi

  if [[ "$db_url" == postgresql* ]]; then
    DB_URL="$db_url" python3 - <<'PY' || {
import os, sys, socket
from urllib.parse import urlparse
url = urlparse(os.environ["DB_URL"])
host = url.hostname or "localhost"
port = url.port or 5432
s = socket.socket()
try:
    s.connect((host, port))
    sys.exit(0)
except OSError:
    sys.exit(1)
finally:
    s.close()
PY
      echo "[backend] Postgres not reachable at ${db_url}, falling back to sqlite:///./dev.db for local dev."
      db_url="sqlite:///./dev.db"
      ENV_PATH="$ENV_FILE" NEW_DB_URL="$db_url" python3 - <<'PY'
import os
from pathlib import Path
env_path = Path(os.environ["ENV_PATH"])
new_db = os.environ["NEW_DB_URL"]
lines = env_path.read_text().splitlines()
new_lines = []
db_set = False
for line in lines:
    if line.startswith("DATABASE_URL="):
        new_lines.append(f"DATABASE_URL={new_db}")
        db_set = True
    else:
        new_lines.append(line)
if not db_set:
    new_lines.append(f"DATABASE_URL={new_db}")
env_path.write_text("\n".join(new_lines) + "\n")
PY
    }
  fi
}

ensure_venv
regenerate_env
pick_db_url

cd "$API_DIR"

# Export env vars from .env for Alembic/uvicorn
set -a
source "$ENV_FILE"
set +a

# If using default sqlite dev db, remove stale file so initial migration can run cleanly
if [ "${DATABASE_URL:-}" = "sqlite:///./dev.db" ] && [ -f "$API_DIR/dev.db" ]; then
  echo "[backend] Removing existing dev.db to apply migrations fresh..."
  rm "$API_DIR/dev.db"
fi

echo "[backend] Running Alembic migrations..."
if alembic upgrade head >/dev/null; then
  echo "[backend] Migrations applied."
else
  echo "[backend] Migrations failed." >&2
  exit 1
fi

echo "[backend] Starting API on http://localhost:8000 ..."
uvicorn app.main:app --reload --port 8000
