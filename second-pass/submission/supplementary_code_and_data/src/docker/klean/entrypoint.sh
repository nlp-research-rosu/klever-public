#!/usr/bin/env bash
set -uo pipefail

FROZEN_TOOLCHAIN_CHECK="${FROZEN_TOOLCHAIN_CHECK:-/usr/local/bin/assert-frozen-toolchain}"
"$FROZEN_TOOLCHAIN_CHECK" klean || exit 70

: "${PROBLEM_ID:?PROBLEM_ID is required}"
: "${GENERATOR_IMAGE_ID:?GENERATOR_IMAGE_ID is required}"
[[ "$PROBLEM_ID" =~ ^[A-Za-z0-9_-]+$ ]] || {
  echo "invalid problem ID" >&2
  exit 2
}
[[ -d /frozen-k && ! -L /frozen-k ]] || exit 2
[[ -d /output && ! -L /output ]] || exit 2
[[ -f /discovery-manifest.json && ! -L /discovery-manifest.json ]] || exit 2
DESTINATION="/output/generation"
[[ ! -e "$DESTINATION" && ! -L "$DESTINATION" ]] || {
  echo "generation already exists: $DESTINATION" >&2
  exit 2
}

LOG="$(mktemp)"
cleanup() { rm -f -- "$LOG"; }
trap cleanup EXIT

set +e
python3 /opt/humaneval/tools/klean_export.py \
  --input /frozen-k \
  --discovery-manifest /discovery-manifest.json \
  --output "$DESTINATION" \
  --problem "$PROBLEM_ID" \
  --generator-image-id "$GENERATOR_IMAGE_ID" \
  --toolchain-lock /opt/humaneval/data/klean-toolchain.lock.json \
  >"$LOG" 2>&1
EXPORT_RC=$?
set -e
if [[ "$EXPORT_RC" -ne 0 ]]; then
  mkdir -- "$DESTINATION"
  cp -- "$LOG" "$DESTINATION/export.log"
  python3 - "$DESTINATION/preflight.json" "$EXPORT_RC" "$LOG" \
    /frozen-k /discovery-manifest.json <<'PY'
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, "/opt/humaneval")
from tools.klean_export import tree_digest

log = Path(sys.argv[3]).read_bytes()
Path(sys.argv[1]).write_text(json.dumps({
    "schema_version": 3,
    "status": "KLEAN_PREFLIGHT_ERROR",
    "error": f"export exited {sys.argv[2]}",
    "export_log_sha256": hashlib.sha256(log).hexdigest(),
    "stage1_workspace_sha256": tree_digest(Path(sys.argv[4])),
    "stage3_discovery_manifest_sha256": hashlib.sha256(
        Path(sys.argv[5]).read_bytes()
    ).hexdigest(),
}, indent=2, sort_keys=True) + "\n")
PY
  exit "$EXPORT_RC"
fi
cp -- "$LOG" "$DESTINATION/export.log"

set +e
python3 /opt/humaneval/tools/klean_preflight.py \
  --input /frozen-k \
  --discovery-manifest /discovery-manifest.json \
  --generation "$DESTINATION" \
  --toolchain-lock /opt/humaneval/data/klean-toolchain.lock.json \
  >>"$LOG" 2>&1
PREFLIGHT_RC=$?
set -e
cp -- "$LOG" "$DESTINATION/preflight.log"
exit "$PREFLIGHT_RC"
