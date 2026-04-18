#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
APP_FILE="$PROJECT_ROOT/app.py"

PORT="${1:-8501}"
HOST="${STREAMLIT_HOST:-127.0.0.1}"
API_URL="${ACADIQ_API_URL:-http://127.0.0.1:8000}"

if [[ ! -f "$APP_FILE" ]]; then
  echo "Error: Streamlit app file not found at $APP_FILE" >&2
  exit 1
fi

if command -v streamlit >/dev/null 2>&1; then
  STREAMLIT_CMD=(streamlit)
else
  PYTHON_BIN="${PYTHON_BIN:-python3}"
  STREAMLIT_CMD=("$PYTHON_BIN" -m streamlit)
fi

export ACADIQ_API_URL="$API_URL"

cd "$PROJECT_ROOT"

echo "Starting Streamlit..."
echo "  App: $APP_FILE"
echo "  Host: $HOST"
echo "  Port: $PORT"
echo "  Backend API: $ACADIQ_API_URL"

exec "${STREAMLIT_CMD[@]}" run "$APP_FILE" \
  --server.address "$HOST" \
  --server.port "$PORT" \
  --server.headless true
