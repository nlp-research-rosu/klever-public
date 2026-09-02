#!/usr/bin/env bash
set -euo pipefail

echo '$ printenv AUDIT_MODE'
printenv AUDIT_MODE
echo '$ read launcher identity fields'
python3 - <<'PY'
import json
from pathlib import Path
doc = json.loads(Path("/audit-input.json").read_text())
r = doc["resolution"]
for key in ("problem_id", "condition", "mode", "semantics_mode"):
    print(f"{key}={r[key]}")
PY
echo '$ kompile --version'
kompile --version
echo '$ kprove --version'
kprove --version
echo '$ pinned Lean/Lake versions with procfs PID compatibility preload'
preload=/tmp/audit-work/lean-hostpid-preload.so
lean_root=/opt/elan/toolchains/leanprover--lean4---v4.22.0
LD_PRELOAD="$preload" "$lean_root/bin/lean" --version
LD_PRELOAD="$preload" "$lean_root/bin/lake" --version
echo '$ test candidate mount absence'
if [[ -e /candidate || -L /candidate ]]; then
  stat /candidate
  exit 1
else
  echo '/candidate ABSENT'
fi
