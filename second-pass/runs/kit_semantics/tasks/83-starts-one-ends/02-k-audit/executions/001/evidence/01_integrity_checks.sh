#!/usr/bin/env bash
set -uo pipefail

log_path=/audit-output/evidence/01_integrity_checks.log
manifest_dir=/audit-output/evidence/integrity-manifests
mkdir -p "$manifest_dir"
exec >"$log_path" 2>&1

run() {
    printf '\n$'
    printf ' %q' "$@"
    printf '\n'
    "$@"
    local status=$?
    printf '[exit %d]\n' "$status"
    return 0
}

printf 'Reviewer integrity checks (UTC): '
date -u +%Y-%m-%dT%H:%M:%SZ

required_paths=(
    /audit-input.json
    /audit-campaign-lock.json
    /run.json
    /task.json
    /generation-result.json
    /generation-evidence/invocation.json
    /generation-evidence/metrics.json
    /generation-evidence/runtime-metrics.json
    /generation-evidence/usage.json
    /generation-evidence/codex-last.txt
    /generation-evidence/codex-output.log
    /generation-evidence/prompt.txt
    /generation-evidence/codex-trace
    /candidate
    /candidate/prompt.py
    /candidate/py2mpy.py
    /candidate/reference-semantics
    /reference/canonical.py
    /reference/prompt.py
    /reference/py2mpy.py
    /reference/reference-semantics
)

for path in "${required_paths[@]}"; do
    run stat -c '%F | mode=%a | size=%s | %n' "$path"
    run test -r "$path"
done

hash_paths=(
    /audit-campaign-lock.json
    /run.json
    /task.json
    /generation-result.json
    /generation-evidence/invocation.json
    /generation-evidence/metrics.json
    /generation-evidence/runtime-metrics.json
    /generation-evidence/usage.json
    /generation-evidence/codex-last.txt
    /generation-evidence/codex-output.log
    /generation-evidence/prompt.txt
    /reference/canonical.py
    /reference/prompt.py
    /reference/py2mpy.py
    /candidate/prompt.py
    /candidate/py2mpy.py
)
run sha256sum "${hash_paths[@]}"

run python3 - /audit-input.json /audit-campaign-lock.json <<'PY'
import hashlib
import json
import sys

audit_path, lock_path = sys.argv[1:]
with open(audit_path, "rb") as stream:
    audit_raw = stream.read()
with open(lock_path, "rb") as stream:
    lock_raw = stream.read()
audit = json.loads(audit_raw)
lock = json.loads(lock_raw)
print("record_layout =", audit.get("record_layout"))
print("semantics_mode =", audit.get("semantics_mode"))
print("campaign_structural_equal =", audit.get("audit_campaign") == lock)
print("lock_actual_sha256 =", hashlib.sha256(lock_raw).hexdigest())
print("lock_recorded_sha256 =", audit.get("hashes", {}).get("audit_campaign_lock_sha256"))
print("container_paths:")
for key, value in sorted(audit.get("container_paths", {}).items()):
    print(f"  {key}={value}")
PY

run cmp -s /candidate/prompt.py /reference/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py
run diff -qr --no-dereference /candidate/reference-semantics /reference/reference-semantics
run find /candidate/reference-semantics -type l -print
run find /reference/reference-semantics -type l -print

find /candidate/reference-semantics -type f -printf '%P\0' \
    | sort -z \
    | while IFS= read -r -d '' rel; do
        sha256sum "/candidate/reference-semantics/$rel"
      done >"$manifest_dir/candidate-reference-semantics.sha256"
find /reference/reference-semantics -type f -printf '%P\0' \
    | sort -z \
    | while IFS= read -r -d '' rel; do
        sha256sum "/reference/reference-semantics/$rel"
      done >"$manifest_dir/trusted-reference-semantics.sha256"
find /generation-evidence/codex-trace -type f -printf '%P\0' \
    | sort -z \
    | while IFS= read -r -d '' rel; do
        sha256sum "/generation-evidence/codex-trace/$rel"
      done >"$manifest_dir/generation-trace.sha256"
find /candidate \
    -path '/candidate/runtime-kompiled' -prune -o \
    -path '/candidate/verification-kompiled' -prune -o \
    -path '/candidate/__pycache__' -prune -o \
    -type f -printf '%P\0' \
    | sort -z \
    | while IFS= read -r -d '' rel; do
        sha256sum "/candidate/$rel"
      done >"$manifest_dir/candidate-source.sha256"

run wc -l \
    "$manifest_dir/candidate-reference-semantics.sha256" \
    "$manifest_dir/trusted-reference-semantics.sha256" \
    "$manifest_dir/generation-trace.sha256" \
    "$manifest_dir/candidate-source.sha256"
run sed -n 1,120p "$manifest_dir/generation-trace.sha256"
run find /candidate -xdev -type l -printf '%p -> %l\n'
run find /generation-evidence -xdev -type l -printf '%p -> %l\n'
run find /reference -xdev -type l -printf '%p -> %l\n'

run python3 - /audit-input.json /generation-result.json <<'PY'
import hashlib
import json
import os
import sys

audit_path, result_path = sys.argv[1:]
audit = json.load(open(audit_path, encoding="utf-8"))
result = json.load(open(result_path, encoding="utf-8"))
paths = {
    "audit_campaign_lock_sha256": "/audit-campaign-lock.json",
    "canonical_sha256": "/reference/canonical.py",
    "trusted_prompt_sha256": "/reference/prompt.py",
    "candidate_prompt_sha256": "/candidate/prompt.py",
    "trusted_translator_sha256": "/reference/py2mpy.py",
    "candidate_translator_sha256": "/candidate/py2mpy.py",
    "run_manifest_sha256": "/run.json",
    "task_manifest_sha256": "/task.json",
    "stage1_result_sha256": "/generation-result.json",
    "stage1_invocation_sha256": "/generation-evidence/invocation.json",
    "generation_metrics_sha256": "/generation-evidence/metrics.json",
    "generation_runtime_metrics_sha256": "/generation-evidence/runtime-metrics.json",
    "generation_usage_sha256": "/generation-evidence/usage.json",
    "generation_codex_last_sha256": "/generation-evidence/codex-last.txt",
    "generation_codex_output_sha256": "/generation-evidence/codex-output.log",
    "generation_prompt_sha256": "/generation-evidence/prompt.txt",
}
recorded = audit["hashes"]
print("audit-input declared single-file hash comparisons:")
all_ok = True
for key, path in paths.items():
    actual = hashlib.sha256(open(path, "rb").read()).hexdigest()
    expected = recorded.get(key)
    ok = actual == expected
    all_ok &= ok
    print(f"{key}: ok={ok} actual={actual} expected={expected} path={path}")
print("all_declared_single_file_hashes_match =", all_ok)

print("generation-result evidence hash comparisons:")
root = "/generation-evidence"
all_result_ok = True
for rel, expected in sorted(result["outputs"]["evidence"].items()):
    path = os.path.join(root, rel)
    actual = hashlib.sha256(open(path, "rb").read()).hexdigest()
    ok = actual == expected
    all_result_ok &= ok
    print(f"{rel}: ok={ok} actual={actual} expected={expected}")
print("all_generation_result_evidence_hashes_match =", all_result_ok)
PY

printf '\nScript exit: 0\n'
