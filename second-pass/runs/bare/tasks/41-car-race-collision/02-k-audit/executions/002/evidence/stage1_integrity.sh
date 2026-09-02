#!/usr/bin/env bash
set -u

run() {
  echo "\$ $*"
  "$@"
  status=$?
  echo "[exit $status]"
  return "$status"
}

run sha256sum \
  /audit-campaign-lock.json \
  /run.json \
  /task.json \
  /generation-result.json \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /generation-evidence/usage.json

run find /generation-evidence/codex-trace -type f -exec sha256sum '{}' +

run python3 -c '
import json
from pathlib import Path

audit_input = json.loads(Path("/audit-input.json").read_text())
campaign_lock = json.loads(Path("/audit-campaign-lock.json").read_text())
print("campaign_block_equal", audit_input["audit_campaign"] == campaign_lock)
print("record_layout", audit_input["record_layout"])
print("semantics_mode", audit_input["semantics_mode"])
required = [
    "/audit-input.json",
    "/audit-campaign-lock.json",
    "/run.json",
    "/task.json",
    "/generation-result.json",
    "/generation-evidence/invocation.json",
    "/generation-evidence/metrics.json",
    "/generation-evidence/codex-last.txt",
    "/generation-evidence/codex-output.log",
    "/generation-evidence/prompt.txt",
    "/generation-evidence/usage.json",
]
for name in required:
    path = Path(name)
    print("regular_non_symlink", path.is_file() and not path.is_symlink(), name)
print(
    "reference_semantics_absent",
    not Path("/reference/reference-semantics").exists()
    and not Path("/reference/reference-semantics").is_symlink(),
)
'

run cmp /candidate/prompt.py /reference/prompt.py
run cmp /candidate/py2mpy.py /reference/py2mpy.py

run find /candidate /generation-evidence /reference -type l -print

run env PYTHONPATH=/opt/humaneval/tools python3 -c '
from pathlib import Path
from pipeline_contract import sha256_tree

print("candidate_sha256_tree", sha256_tree(Path("/candidate")))
print("trace_sha256_tree", sha256_tree(Path("/generation-evidence/codex-trace")))
'
