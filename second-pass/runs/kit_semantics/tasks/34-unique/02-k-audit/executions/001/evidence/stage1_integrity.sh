#!/usr/bin/env bash
set -uo pipefail

log=/audit-output/evidence/stage1_integrity.log
exec >"$log" 2>&1

run() {
  echo "COMMAND: $*"
  "$@"
  status=$?
  echo "EXIT: $status"
  return "$status"
}

echo "STAGE 1 INPUT AND PROVENANCE INTEGRITY"
run stat -c '%F %a %U:%G %n -> %N' \
  /audit-input.json \
  /audit-campaign-lock.json \
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
  /generation-evidence/codex-trace \
  /candidate \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /reference/reference-semantics

run sha256sum \
  /audit-campaign-lock.json \
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
  /generation-evidence/codex-trace/2026/07/30/rollout-2026-07-30T02-20-25-019fb1e5-58a2-72d3-9f48-d3ea21a181e5.jsonl \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py

echo "COMMAND: compare campaign JSON, declared mode/layout, required record types, and parse every JSONL trace event"
python3 - <<'PY'
import json
import os
import stat
from collections import Counter

with open("/audit-input.json", encoding="utf-8") as stream:
    audit = json.load(stream)
with open("/audit-campaign-lock.json", encoding="utf-8") as stream:
    lock = json.load(stream)

print("campaign_json_equal", audit["audit_campaign"] == lock)
print("record_layout", audit["record_layout"])
print("semantics_mode", audit["semantics_mode"])

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
    "/generation-evidence/codex-trace",
]
for path in required:
    info = os.lstat(path)
    kind = "directory" if stat.S_ISDIR(info.st_mode) else "regular" if stat.S_ISREG(info.st_mode) else "other"
    print("record", path, kind, "symlink", stat.S_ISLNK(info.st_mode), "readable", os.access(path, os.R_OK))

trace_path = "/generation-evidence/codex-trace/2026/07/30/rollout-2026-07-30T02-20-25-019fb1e5-58a2-72d3-9f48-d3ea21a181e5.jsonl"
outer = Counter()
payload = Counter()
line_count = 0
with open(trace_path, encoding="utf-8") as stream:
    for line_count, line in enumerate(stream, 1):
        event = json.loads(line)
        outer[event.get("type")] += 1
        body = event.get("payload")
        if isinstance(body, dict):
            payload[body.get("type")] += 1
print("trace_lines", line_count)
print("trace_outer_types", sorted(outer.items(), key=lambda item: str(item[0])))
print("trace_payload_types", sorted(payload.items(), key=lambda item: str(item[0])))
PY
echo "EXIT: $?"

echo "COMMAND: independently compute launcher pipeline tree digests for mounted trees"
python3 - <<'PY'
import sys
from pathlib import Path

sys.path.insert(0, "/opt/humaneval/tools")
import pipeline_contract

for path in [
    "/candidate",
    "/reference/reference-semantics",
    "/candidate/reference-semantics",
    "/generation-evidence/codex-trace",
]:
    print(path, pipeline_contract.sha256_tree(Path(path)))
PY
echo "EXIT: $?"

echo "COMMAND: find candidate and trusted semantics symlinks"
find /candidate/reference-semantics /reference/reference-semantics -type l -printf '%p -> %l\n'
status=$?
echo "EXIT: $status"

run cmp /reference/prompt.py /candidate/prompt.py
run cmp /reference/py2mpy.py /candidate/py2mpy.py
run diff --no-dereference -ru /reference/reference-semantics /candidate/reference-semantics

echo "COMMAND: independent trusted supplied-semantics manifest"
find /reference/reference-semantics -type f -printf '%P\0' |
  sort -z |
  xargs -0 -I{} sha256sum '/reference/reference-semantics/{}'
status=$?
echo "EXIT: $status"

echo "COMMAND: independent candidate supplied-semantics manifest"
find /candidate/reference-semantics -type f -printf '%P\0' |
  sort -z |
  xargs -0 -I{} sha256sum '/candidate/reference-semantics/{}'
status=$?
echo "EXIT: $status"
