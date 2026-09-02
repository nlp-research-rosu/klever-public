#!/usr/bin/env bash
set -u
set -o pipefail
PS4='+ command: '
set -x

sha256sum \
  /audit-campaign-lock.json \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/runtime-metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /generation-evidence/codex-trace/2026/07/25/rollout-2026-07-25T02-26-36-019f982b-3454-72a0-9280-99e7bcf6de86.jsonl
printf 'sha256sum_exit=%s\n' "$?"

stat -c '%F %a %s %n' \
  /audit-input.json \
  /audit-campaign-lock.json \
  /candidate \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /reference/reference-semantics \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/runtime-metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /generation-evidence/codex-trace
printf 'stat_exit=%s\n' "$?"

find /candidate /reference /generation-evidence -type l -printf '%p -> %l\n'
printf 'symlink_scan_exit=%s\n' "$?"

cmp -s /candidate/prompt.py /reference/prompt.py
printf 'prompt_cmp_exit=%s\n' "$?"
cmp -s /candidate/py2mpy.py /reference/py2mpy.py
printf 'translator_cmp_exit=%s\n' "$?"
diff -r --no-dereference --brief \
  /candidate/reference-semantics \
  /reference/reference-semantics
printf 'semantics_diff_exit=%s\n' "$?"

find /reference/reference-semantics -type f -printf '%P\n' | LC_ALL=C sort
printf 'trusted_semantics_manifest_exit=%s\n' "$?"
find /candidate/reference-semantics -type f -printf '%P\n' | LC_ALL=C sort
printf 'candidate_semantics_manifest_exit=%s\n' "$?"

python3 - <<'PY'
import json
from pathlib import Path

audit = json.loads(Path("/audit-input.json").read_text())
lock = json.loads(Path("/audit-campaign-lock.json").read_text())
print("record_layout=", audit["record_layout"])
print("semantics_mode=", audit["semantics_mode"])
print("campaign_object_equal=", audit["audit_campaign"] == lock)
print(
    "recorded_lock_hash=",
    audit["hashes"]["audit_campaign_lock_sha256"],
)
required = [
    "/run.json",
    "/task.json",
    "/generation-result.json",
    "/generation-evidence/invocation.json",
    "/generation-evidence/metrics.json",
    "/generation-evidence/runtime-metrics.json",
    "/generation-evidence/usage.json",
    "/generation-evidence/codex-last.txt",
    "/generation-evidence/codex-output.log",
    "/generation-evidence/prompt.txt",
]
for raw in required:
    path = Path(raw)
    print(
        "required_record",
        raw,
        "exists=", path.exists(),
        "file=", path.is_file(),
        "readable=", path.open("rb").read(1) is not None,
    )
PY
printf 'json_integrity_exit=%s\n' "$?"

