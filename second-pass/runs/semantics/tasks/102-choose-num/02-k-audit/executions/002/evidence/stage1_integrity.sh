#!/usr/bin/env bash
set -uo pipefail

status=0

printf '%s\n' '$ sha256sum launcher-owned files and mounted provenance inputs'
sha256sum \
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
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/codex-trace/2026/07/23/*.jsonl || status=1

printf '%s\n' '$ compare campaign block with audit-campaign-lock.json'
python3 - <<'PY' || status=1
import hashlib
import json

with open("/audit-input.json", "rb") as stream:
    audit_bytes = stream.read()
with open("/audit-campaign-lock.json", "rb") as stream:
    lock_bytes = stream.read()
audit = json.loads(audit_bytes)
lock = json.loads(lock_bytes)
actual_hash = hashlib.sha256(lock_bytes).hexdigest()
print("record_layout", audit["record_layout"])
print("semantics_mode", audit["semantics_mode"])
print("campaign_block_equal", audit["audit_campaign"] == lock)
print("lock_hash_recorded", audit["hashes"]["audit_campaign_lock_sha256"])
print("lock_hash_actual", actual_hash)
assert audit["audit_campaign"] == lock
assert audit["hashes"]["audit_campaign_lock_sha256"] == actual_hash
PY

printf '%s\n' '$ require all legacy-selected-stage1 records and provenance mounts'
python3 - <<'PY' || status=1
import json
import os
import stat

with open("/audit-input.json") as stream:
    audit = json.load(stream)
required = [
    "/audit-input.json",
    "/audit-campaign-lock.json",
    "/run.json",
    "/task.json",
    "/generation-result.json",
    "/generation-evidence/invocation.json",
    "/generation-evidence/metrics.json",
    "/generation-evidence/usage.json",
    "/generation-evidence/codex-last.txt",
    "/generation-evidence/codex-output.log",
    "/generation-evidence/prompt.txt",
    "/generation-evidence/codex-trace",
    "/candidate",
    "/reference/canonical.py",
    "/reference/prompt.py",
    "/reference/py2mpy.py",
    "/reference/reference-semantics",
]
required.extend(audit["container_paths"].values())
for path in sorted(set(required)):
    st = os.lstat(path)
    assert not stat.S_ISLNK(st.st_mode), path
    assert os.access(path, os.R_OK), path
    print(stat.filemode(st.st_mode), st.st_size, path)
PY

printf '%s\n' '$ cmp candidate prompt and translator against trusted mounts'
cmp /candidate/prompt.py /reference/prompt.py || status=1
printf 'candidate_prompt_cmp_exit=%s\n' "$?"
cmp /candidate/py2mpy.py /reference/py2mpy.py || status=1
printf 'candidate_translator_cmp_exit=%s\n' "$?"

printf '%s\n' '$ recursively compare supplied candidate semantics with trusted semantics'
diff -r --no-dereference \
  /reference/reference-semantics \
  /candidate/reference-semantics || status=1
printf 'reference_semantics_diff_exit=%s\n' "$?"

printf '%s\n' '$ reject symlinks anywhere in candidate supplied-semantics tree'
symlinks="$(find /candidate/reference-semantics -type l -print)"
if [[ -n "$symlinks" ]]; then
  printf '%s\n' "$symlinks"
  status=1
else
  printf '%s\n' 'candidate_reference_semantics_symlinks=0'
fi

printf '%s\n' '$ validate all structured trace lines as JSON'
python3 - <<'PY' || status=1
import json
from collections import Counter
from pathlib import Path

paths = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
files = [path for path in paths if path.is_file()]
assert files
total = 0
counts = Counter()
for path in files:
    with path.open() as stream:
        for line_number, line in enumerate(stream, 1):
            event = json.loads(line)
            total += 1
            counts[event.get("type", "<missing>")] += 1
    print("trace_file", path, "lines", line_number)
print("trace_total_valid_json_lines", total)
print("trace_top_level_type_counts", dict(sorted(counts.items())))
PY

printf 'stage1_integrity_exit=%s\n' "$status"
exit "$status"
