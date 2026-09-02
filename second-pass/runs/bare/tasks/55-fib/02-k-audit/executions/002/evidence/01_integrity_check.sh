#!/usr/bin/env bash
set -euo pipefail

required_regular=(
  /audit-input.json
  /audit-campaign-lock.json
  /run.json
  /task.json
  /generation-result.json
  /generation-evidence/invocation.json
  /generation-evidence/metrics.json
  /generation-evidence/usage.json
  /generation-evidence/codex-last.txt
  /generation-evidence/codex-output.log
  /generation-evidence/prompt.txt
  /generation-evidence/codex-trace/2026/07/22/rollout-2026-07-22T05-11-27-019f894f-0f4b-7912-adc3-c85b88e6a8cd.jsonl
  /reference/canonical.py
  /reference/prompt.py
  /reference/py2mpy.py
  /candidate/prompt.py
  /candidate/py2mpy.py
  /candidate/solution.py
  /candidate/solution.mpy
  /candidate/semantic.k
  /candidate/verification.k
  /candidate/spec.k
  /candidate/prove.sh
)

for artifact in "${required_regular[@]}"; do
  test -f "$artifact"
  test ! -L "$artifact"
  test -r "$artifact"
  printf 'REGULAR_READABLE %s\n' "$artifact"
done

sha256sum \
  /audit-campaign-lock.json \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /generation-evidence/codex-trace/2026/07/22/rollout-2026-07-22T05-11-27-019f894f-0f4b-7912-adc3-c85b88e6a8cd.jsonl \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py

cmp /candidate/prompt.py /reference/prompt.py
printf 'MATCH candidate/prompt.py reference/prompt.py\n'
cmp /candidate/py2mpy.py /reference/py2mpy.py
printf 'MATCH candidate/py2mpy.py reference/py2mpy.py\n'

test ! -e /reference/reference-semantics
test ! -e /candidate/reference-semantics
printf 'GENERATED_SEMANTICS_BOUNDARY reference-semantics absent in trusted and candidate trees\n'

python3 - <<'PY'
import json
from pathlib import Path

audit = json.loads(Path("/audit-input.json").read_text())
lock = json.loads(Path("/audit-campaign-lock.json").read_text())
assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
assert audit["audit_campaign"] == lock
assert audit["hashes"]["audit_campaign_lock_sha256"] == "ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745"
print("JSON campaign_object_equal=True")
print("JSON record_layout=legacy-selected-stage1")
print("JSON semantics_mode=GENERATED_SEMANTICS")
PY

PYTHONPATH=/opt/humaneval/tools python3 - <<'PY'
from pathlib import Path
import pipeline_contract

print("PIPELINE_SHA256_TREE candidate", pipeline_contract.sha256_tree(Path("/candidate")))
print("PIPELINE_SHA256_TREE generation-trace", pipeline_contract.sha256_tree(Path("/generation-evidence/codex-trace")))
PY

if find /candidate /generation-evidence /reference -type l -print -quit | grep -q .; then
  echo "UNEXPECTED_SYMLINK"
  exit 1
fi
printf 'NO_SYMLINKS candidate generation-evidence reference\n'
