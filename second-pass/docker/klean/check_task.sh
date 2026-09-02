#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
if [[ $# -ne 3 ]]; then
  echo "usage: check_task.sh <run-id> <problem> <generation-id>" >&2
  exit 2
fi
DISCOVERY_MANIFEST="$(
  python3 - "$REPO" "$1" "$2" <<'PY'
import sys
from pathlib import Path

repo = Path(sys.argv[1])
sys.path.insert(0, str(repo))
from tools import pipeline_contract, stage4_runner

task, _state, _run = pipeline_contract._resolve_task_state(
    repo, sys.argv[2], sys.argv[3]
)
print(stage4_runner._protected_stage3_discovery(task).path)
PY
)"
exec python3 "$REPO/tools/klean_preflight.py" \
  --input "$REPO/runs/$1/tasks/$2/01-k-proof/workspace" \
  --discovery-manifest "$DISCOVERY_MANIFEST" \
  --generation "$REPO/runs/$1/tasks/$2/04-klean-generation/generations/$3" \
  --toolchain-lock "$REPO/data/klean-toolchain.lock.json"
