#!/usr/bin/env bash
set -u

status=0

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf 'EXIT: %d\n' "$rc"
  if [[ "$rc" -ne 0 ]]; then
    status=1
  fi
}

required=(
  /audit-input.json
  /audit-campaign-lock.json
  /run.json
  /task.json
  /generation-result.json
  /generation-evidence/invocation.json
  /generation-evidence/metrics.json
  /generation-evidence/codex-last.txt
  /generation-evidence/codex-output.log
  /generation-evidence/prompt.txt
  /generation-evidence/usage.json
  /reference/canonical.py
  /reference/prompt.py
  /reference/py2mpy.py
  /candidate/prompt.py
  /candidate/py2mpy.py
)

for path in "${required[@]}"; do
  run test -f "$path"
  run test ! -L "$path"
done

run test -d /candidate
run test ! -L /candidate
run test -d /generation-evidence/codex-trace
run test ! -L /generation-evidence/codex-trace
run test ! -e /reference/reference-semantics

run cmp -s /candidate/prompt.py /reference/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py

run sha256sum \
  /audit-campaign-lock.json \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /generation-evidence/codex-trace/2026/07/22/rollout-2026-07-22T03-47-52-019f8902-899a-77b0-80ed-82a38b5648a8.jsonl \
  /run.json \
  /task.json \
  /generation-result.json

printf '%s\n' '$ python3 - (campaign JSON semantic comparison)'
python3 - <<'PY'
import json

with open("/audit-input.json", encoding="utf-8") as stream:
    audit_input = json.load(stream)
with open("/audit-campaign-lock.json", encoding="utf-8") as stream:
    campaign_lock = json.load(stream)

print(f"campaign_content_equal={audit_input['audit_campaign'] == campaign_lock}")
print(f"record_layout={audit_input['record_layout']}")
print(f"semantics_mode={audit_input['semantics_mode']}")
if audit_input["audit_campaign"] != campaign_lock:
    raise SystemExit(1)
PY
rc=$?
printf 'EXIT: %d\n' "$rc"
if [[ "$rc" -ne 0 ]]; then
  status=1
fi

printf '%s\n' '$ PYTHONPATH=/opt/humaneval/tools python3 - (pipeline tree hashes)'
PYTHONPATH=/opt/humaneval/tools python3 - <<'PY'
from pathlib import Path

import pipeline_contract

print("candidate_sha256_tree=" + pipeline_contract.sha256_tree(Path("/candidate")))
print(
    "trace_sha256_tree="
    + pipeline_contract.sha256_tree(Path("/generation-evidence/codex-trace"))
)
PY
rc=$?
printf 'EXIT: %d\n' "$rc"
if [[ "$rc" -ne 0 ]]; then
  status=1
fi

printf '%s\n' '$ find /candidate /reference /generation-evidence -type l -print'
find /candidate /reference /generation-evidence -type l -print
rc=$?
printf 'EXIT: %d\n' "$rc"
if [[ "$rc" -ne 0 ]]; then
  status=1
fi

exit "$status"
