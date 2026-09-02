#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT: %d\n' "$status"
  return "$status"
}

run sha256sum \
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
  /generation-evidence/codex-trace/2026/07/22/rollout-2026-07-22T20-56-12-019f8cb0-0069-7ac1-9a56-db31e2036496.jsonl \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py

run python3 -c '
import json
a=json.load(open("/audit-input.json"))
l=json.load(open("/audit-campaign-lock.json"))
assert a["audit_campaign"] == l
assert a["record_layout"] == "legacy-selected-stage1"
assert a["semantics_mode"] == "SUPPLIED_SEMANTICS"
print("campaign_block_equal=true")
print("record_layout=legacy-selected-stage1")
print("semantics_mode=SUPPLIED_SEMANTICS")
'

run cmp /candidate/prompt.py /reference/prompt.py
run cmp /candidate/py2mpy.py /reference/py2mpy.py
run diff -qr --no-dereference /candidate/reference-semantics /reference/reference-semantics

run python3 -c '
from pathlib import Path
roots=[Path("/candidate/reference-semantics"),Path("/reference/reference-semantics")]
for root in roots:
    entries=sorted(root.rglob("*"))
    bad=[str(p) for p in entries if p.is_symlink() or not (p.is_dir() or p.is_file())]
    print(f"{root}: entries={len(entries)} irregular_or_symlinked={bad}")
'

run python3 -c '
import hashlib
from pathlib import Path
for root in (Path("/candidate/reference-semantics"), Path("/reference/reference-semantics")):
    print(root)
    for p in sorted(x for x in root.rglob("*") if x.is_file()):
        print(hashlib.sha256(p.read_bytes()).hexdigest(), p.relative_to(root))
'
