#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
exec python3 "$REPO/tools/stage4_runner.py" --repo "$REPO" "$@"
