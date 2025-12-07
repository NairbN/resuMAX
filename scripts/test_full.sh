#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Running backend tests..."
cd "$ROOT_DIR"
./scripts/test_api.sh

echo "Running frontend tests..."
./scripts/test_frontend.sh
