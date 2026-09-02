#!/usr/bin/env bash
set -u

record() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

required_files=(
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
  /reference/canonical.py
  /reference/prompt.py
  /reference/py2mpy.py
  /candidate/prompt.py
  /candidate/py2mpy.py
  /candidate/solution.py
  /candidate/solution.mpy
  /candidate/verification.k
  /candidate/spec.k
  /candidate/prove.sh
)

record python3 -c '
import json
from pathlib import Path
a = json.loads(Path("/audit-input.json").read_text())
l = json.loads(Path("/audit-campaign-lock.json").read_text())
print("record_layout =", a["record_layout"])
print("semantics_mode =", a["semantics_mode"])
print("campaign_block_exact_match =", a["audit_campaign"] == l)
print("declared_campaign_hash =", a["hashes"]["audit_campaign_lock_sha256"])
'

for path in "${required_files[@]}"; do
  record stat -c '%F|%s|%a|%n' "$path"
  record test -f "$path"
  record test ! -L "$path"
done

record sha256sum \
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
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py

record python3 -c '
import hashlib, json
from pathlib import Path
a = json.loads(Path("/audit-input.json").read_text())
checks = {
    "audit_campaign_lock_sha256": "/audit-campaign-lock.json",
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
    "candidate_prompt_sha256": "/candidate/prompt.py",
    "candidate_translator_sha256": "/candidate/py2mpy.py",
}
for key, path in checks.items():
    got = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    expected = a["hashes"][key]
    print(f"{key}: match={got == expected} expected={expected} got={got}")
'

record cmp -s /candidate/prompt.py /reference/prompt.py
record cmp -s /candidate/py2mpy.py /reference/py2mpy.py
record diff -r --no-dereference /candidate/reference-semantics /reference/reference-semantics
record find -P /candidate/reference-semantics /reference/reference-semantics -type l -printf 'SYMLINK %p -> %l\n'
record find -P /candidate/reference-semantics /reference/reference-semantics \
  ! -type d ! -type f -printf 'NONREGULAR %y %p\n'
record find -P /generation-evidence/codex-trace -type l -printf 'SYMLINK %p -> %l\n'
record find -P /generation-evidence/codex-trace ! -type d ! -type f -printf 'NONREGULAR %y %p\n'
record find -P /generation-evidence/codex-trace -type f -print0

record python3 -c '
import hashlib, json
from pathlib import Path
result = json.loads(Path("/generation-result.json").read_text())
for rel, expected in sorted(result["outputs"]["evidence"].items()):
    path = Path("/generation-evidence") / rel
    ok_type = path.is_file() and not path.is_symlink()
    got = hashlib.sha256(path.read_bytes()).hexdigest() if ok_type else None
    print(f"{rel}: regular={ok_type} match={got == expected} expected={expected} got={got}")
'

record python3 -c '
import hashlib
from pathlib import Path
def manifest(root):
    root = Path(root)
    rows = []
    for p in sorted(root.rglob("*"), key=lambda x: x.relative_to(root).as_posix()):
        rel = p.relative_to(root).as_posix()
        if p.is_symlink():
            rows.append(("l", rel, p.readlink().as_posix()))
        elif p.is_dir():
            rows.append(("d", rel, ""))
        elif p.is_file():
            rows.append(("f", rel, hashlib.sha256(p.read_bytes()).hexdigest()))
        else:
            rows.append(("?", rel, ""))
    return rows
c = manifest("/candidate/reference-semantics")
r = manifest("/reference/reference-semantics")
print("semantic_manifest_entries_candidate =", len(c))
print("semantic_manifest_entries_trusted =", len(r))
print("semantic_manifests_exact_match =", c == r)
for row in c:
    print("|".join(row))
'
