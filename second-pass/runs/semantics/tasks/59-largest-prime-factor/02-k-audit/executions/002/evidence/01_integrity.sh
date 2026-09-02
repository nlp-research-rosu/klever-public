#!/usr/bin/env bash
set -u

run() {
  echo "\$ $*"
  "$@"
  status=$?
  echo "[exit $status]"
  return "$status"
}

echo "== Required mounts and records =="
run stat -c '%F %a %U:%G %n' \
  /audit-input.json \
  /audit-campaign-lock.json \
  /run.json \
  /task.json \
  /generation-result.json \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /reference/reference-semantics \
  /candidate \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /generation-evidence/codex-trace

echo "== Independent file hashes =="
run sha256sum \
  /audit-input.json \
  /audit-campaign-lock.json \
  /run.json \
  /task.json \
  /generation-result.json \
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
  /generation-evidence/codex-trace/2026/07/23/rollout-2026-07-23T00-38-25-019f8d7b-710f-7f03-8454-aa05bfcdc438.jsonl

echo "== Campaign lock and recorded hashes =="
run python3 - <<'PY'
import hashlib
import json
from pathlib import Path

audit = json.loads(Path("/audit-input.json").read_text())
lock_raw = Path("/audit-campaign-lock.json").read_bytes()
lock = json.loads(lock_raw)
actual_lock_hash = hashlib.sha256(lock_raw).hexdigest()
print("record_layout:", audit["record_layout"])
print("semantics_mode:", audit["semantics_mode"])
print("campaign_block_equals_lock:", audit["audit_campaign"] == lock)
print("recorded_lock_hash:", audit["hashes"]["audit_campaign_lock_sha256"])
print("actual_lock_hash:", actual_lock_hash)
print("lock_hash_matches:", actual_lock_hash == audit["hashes"]["audit_campaign_lock_sha256"])

paths = {
    "run_manifest_sha256": "/run.json",
    "task_manifest_sha256": "/task.json",
    "stage1_result_sha256": "/generation-result.json",
    "stage1_invocation_sha256": "/generation-evidence/invocation.json",
    "generation_metrics_sha256": "/generation-evidence/metrics.json",
    "generation_usage_sha256": "/generation-evidence/usage.json",
    "generation_codex_last_sha256": "/generation-evidence/codex-last.txt",
    "generation_codex_output_sha256": "/generation-evidence/codex-output.log",
    "generation_prompt_sha256": "/generation-evidence/prompt.txt",
    "canonical_sha256": "/reference/canonical.py",
    "trusted_prompt_sha256": "/reference/prompt.py",
    "trusted_translator_sha256": "/reference/py2mpy.py",
}
for key, path in paths.items():
    actual = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    expected = audit["hashes"][key]
    print(f"{key}: match={actual == expected} expected={expected} actual={actual} path={path}")
PY

echo "== Candidate/trusted file identity =="
run cmp /candidate/prompt.py /reference/prompt.py
run cmp /candidate/py2mpy.py /reference/py2mpy.py
run diff -qr --no-dereference /candidate/reference-semantics /reference/reference-semantics

echo "== Type and symlink checks =="
run find /candidate/reference-semantics -printf '%y %P -> %l\n'
run find /reference/reference-semantics -printf '%y %P -> %l\n'
run find /candidate -maxdepth 2 -type l -print

echo "== Reviewer-defined normalized semantics hashes =="
run bash -c 'cd /candidate/reference-semantics && find . -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum'
run bash -c 'cd /reference/reference-semantics && find . -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum'

echo "== Structured trace integrity and inventory =="
run python3 - <<'PY'
import collections
import hashlib
import json
from pathlib import Path

p = Path("/generation-evidence/codex-trace/2026/07/23/rollout-2026-07-23T00-38-25-019f8d7b-710f-7f03-8454-aa05bfcdc438.jsonl")
top = collections.Counter()
payload = collections.Counter()
bad = []
last_line = 0
for last_line, line in enumerate(p.open(), 1):
    try:
        event = json.loads(line)
    except Exception as err:
        bad.append((last_line, str(err)))
        continue
    top[event.get("type")] += 1
    body = event.get("payload")
    if isinstance(body, dict):
        payload[(event.get("type"), body.get("type"))] += 1
print("lines:", last_line)
print("invalid_json_lines:", bad)
print("top_level_types:", sorted(top.items(), key=lambda item: str(item[0])))
print("payload_types:", sorted(payload.items(), key=lambda item: str(item[0])))
print("file_sha256:", hashlib.sha256(p.read_bytes()).hexdigest())
PY
