#!/usr/bin/env bash
set -u
overall=0

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  local status=0
  "$@" || status=$?
  printf '[exit %d]\n' "$status"
  if (( status != 0 )); then
    overall=1
  fi
  return 0
}

printf 'AUDIT INPUT AND REQUIRED RECORD TYPES\n'
run stat -c '%F %a %s %n -> %N' \
  /audit-input.json \
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
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/verification.k \
  /candidate/spec.k \
  /candidate/prove.sh

printf 'DECLARED FILE HASHES\n'
run sha256sum \
  /audit-input.json \
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
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/verification.k \
  /candidate/spec.k \
  /candidate/prove.sh

printf 'CAMPAIGN BLOCK DEEP COMPARISON AND RECORDED-HASH CHECKS\n'
run python3 - /audit-input.json /audit-campaign-lock.json <<'PY'
import hashlib
import json
import pathlib
import sys

audit_path = pathlib.Path(sys.argv[1])
lock_path = pathlib.Path(sys.argv[2])
audit = json.loads(audit_path.read_text())
lock = json.loads(lock_path.read_text())

print(f"campaign_deep_equal={audit['audit_campaign'] == lock}")
actual_lock_hash = hashlib.sha256(lock_path.read_bytes()).hexdigest()
print(f"campaign_hash_actual={actual_lock_hash}")
print(f"campaign_hash_recorded={audit['hashes']['audit_campaign_lock_sha256']}")

checks = {
    "/run.json": "run_manifest_sha256",
    "/task.json": "task_manifest_sha256",
    "/generation-result.json": "stage1_result_sha256",
    "/generation-evidence/invocation.json": "stage1_invocation_sha256",
    "/generation-evidence/metrics.json": "generation_metrics_sha256",
    "/generation-evidence/usage.json": "generation_usage_sha256",
    "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
    "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
    "/generation-evidence/prompt.txt": "generation_prompt_sha256",
    "/reference/canonical.py": "canonical_sha256",
    "/reference/prompt.py": "trusted_prompt_sha256",
    "/reference/py2mpy.py": "trusted_translator_sha256",
}
all_match = audit["audit_campaign"] == lock
all_match &= actual_lock_hash == audit["hashes"]["audit_campaign_lock_sha256"]
for name, key in checks.items():
    actual = hashlib.sha256(pathlib.Path(name).read_bytes()).hexdigest()
    expected = audit["hashes"][key]
    matches = actual == expected
    all_match &= matches
    print(f"{name}: key={key} match={matches}")
print(f"all_declared_file_hashes_match={all_match}")
raise SystemExit(0 if all_match else 1)
PY

printf 'REQUIRED LEGACY-SELECTED-STAGE1 GENERATION RECORDS\n'
run python3 - <<'PY'
import pathlib

required = [
    "/run.json",
    "/task.json",
    "/generation-result.json",
    "/generation-evidence/invocation.json",
    "/generation-evidence/metrics.json",
    "/generation-evidence/codex-last.txt",
    "/generation-evidence/codex-output.log",
    "/generation-evidence/prompt.txt",
]
optional = [
    "/generation-evidence/usage.json",
    "/generation-evidence/runtime-metrics.json",
]
ok = True
for name in required:
    path = pathlib.Path(name)
    good = path.is_file() and not path.is_symlink()
    ok &= good
    print(f"required {name}: regular_non_symlink={good}")
for name in optional:
    path = pathlib.Path(name)
    print(f"optional {name}: present={path.exists()} symlink={path.is_symlink()}")
raise SystemExit(0 if ok else 1)
PY

printf 'TRUSTED/CANDIDATE PROMPT AND TRANSLATOR BYTE IDENTITY\n'
run cmp /candidate/prompt.py /reference/prompt.py
run cmp /candidate/py2mpy.py /reference/py2mpy.py
run bash -c 'test "$(find /candidate /reference -type l -print -quit)" = ""'

printf 'SUPPLIED SEMANTICS RECURSIVE IDENTITY\n'
run diff -qr --no-dereference \
  /candidate/reference-semantics \
  /reference/reference-semantics
run bash -c 'test "$(find /candidate/reference-semantics /reference/reference-semantics -type l -print -quit)" = ""'
run bash -c 'cd /candidate/reference-semantics && find . -type f -print0 | sort -z | xargs -0 sha256sum'
run bash -c 'cd /reference/reference-semantics && find . -type f -print0 | sort -z | xargs -0 sha256sum'

printf 'GENERATION TRACE RECORDS AND HASHES\n'
run find /generation-evidence/codex-trace -printf '%y %p %s -> %l\n'
run sha256sum \
  /generation-evidence/codex-trace/2026/07/23/rollout-2026-07-23T02-35-02-019f8de6-3522-7992-a411-c8389da4eabd.jsonl \
  /generation-evidence/legacy-metrics.json \
  /generation-evidence/legacy-run-input.json

printf 'stage1_integrity_status=%d\n' "$overall"
exit "$overall"
