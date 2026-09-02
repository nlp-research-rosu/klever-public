#!/usr/bin/env bash
set -u

failures=0

check_regular() {
  local path="$1"
  if [[ -f "$path" && ! -L "$path" ]]; then
    printf 'OK regular %s\n' "$path"
  else
    printf 'FAIL required regular file %s\n' "$path"
    failures=$((failures + 1))
  fi
}

check_directory() {
  local path="$1"
  if [[ -d "$path" && ! -L "$path" ]]; then
    printf 'OK directory %s\n' "$path"
  else
    printf 'FAIL required directory %s\n' "$path"
    failures=$((failures + 1))
  fi
}

for path in \
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
  /reference/py2mpy.py
do
  check_regular "$path"
done

for path in \
  /candidate \
  /reference/reference-semantics \
  /candidate/reference-semantics \
  /generation-evidence/codex-trace
do
  check_directory "$path"
done

trace_count="$(find /generation-evidence/codex-trace -type f -name '*.jsonl' | wc -l)"
printf 'structured trace JSONL count: %s\n' "$trace_count"
if [[ "$trace_count" -ne 1 ]]; then
  failures=$((failures + 1))
fi

python3 - <<'PY'
import hashlib
import json
from pathlib import Path

audit = json.loads(Path("/audit-input.json").read_text())
lock_bytes = Path("/audit-campaign-lock.json").read_bytes()
lock = json.loads(lock_bytes)
print("record_layout:", audit["record_layout"])
print("semantics_mode:", audit["semantics_mode"])
print("campaign_block_equal:", lock == audit["audit_campaign"])
actual_lock_hash = hashlib.sha256(lock_bytes).hexdigest()
expected_lock_hash = audit["hashes"]["audit_campaign_lock_sha256"]
print("campaign_lock_sha256:", actual_lock_hash)
print("campaign_lock_hash_matches:", actual_lock_hash == expected_lock_hash)

paths = {
    "canonical_sha256": "/reference/canonical.py",
    "trusted_prompt_sha256": "/reference/prompt.py",
    "trusted_translator_sha256": "/reference/py2mpy.py",
    "run_manifest_sha256": "/run.json",
    "task_manifest_sha256": "/task.json",
    "stage1_result_sha256": "/generation-result.json",
    "stage1_invocation_sha256": "/generation-evidence/invocation.json",
    "generation_metrics_sha256": "/generation-evidence/metrics.json",
    "generation_usage_sha256": "/generation-evidence/usage.json",
    "generation_codex_last_sha256": "/generation-evidence/codex-last.txt",
    "generation_codex_output_sha256": "/generation-evidence/codex-output.log",
    "generation_prompt_sha256": "/generation-evidence/prompt.txt",
}
for key, path in paths.items():
    actual = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    expected = audit["hashes"][key]
    print(f"{key}: actual={actual} expected={expected} match={actual == expected}")

result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
for relative, expected in result["outputs"]["evidence"].items():
    mounted = Path("/generation-evidence") / relative
    actual = hashlib.sha256(mounted.read_bytes()).hexdigest()
    print(f"result evidence {relative}: actual={actual} expected={expected} match={actual == expected}")
for relative, expected in invocation["outputs"]["evidence"].items():
    mounted = Path("/generation-evidence") / relative
    actual = hashlib.sha256(mounted.read_bytes()).hexdigest()
    print(f"invocation evidence {relative}: actual={actual} expected={expected} match={actual == expected}")
PY

if cmp -s /candidate/prompt.py /reference/prompt.py; then
  printf 'OK candidate prompt byte-identical to trusted prompt\n'
else
  printf 'FAIL candidate prompt differs\n'
  failures=$((failures + 1))
fi

if cmp -s /candidate/py2mpy.py /reference/py2mpy.py; then
  printf 'OK candidate translator byte-identical to trusted translator\n'
else
  printf 'FAIL candidate translator differs\n'
  failures=$((failures + 1))
fi

if diff -r --no-dereference --brief \
    /candidate/reference-semantics /reference/reference-semantics; then
  printf 'OK candidate supplied-semantics tree byte-identical\n'
else
  printf 'FAIL candidate supplied-semantics tree differs\n'
  failures=$((failures + 1))
fi

for root in /candidate/reference-semantics /reference/reference-semantics; do
  printf 'ENTRY MANIFEST %s\n' "$root"
  find "$root" -printf '%y %m %P -> %l\n' | LC_ALL=C sort
  printf 'FILE HASH MANIFEST %s\n' "$root"
  while IFS= read -r -d '' file; do
    rel="${file#"$root"/}"
    printf '%s  %s\n' "$(sha256sum "$file" | cut -d' ' -f1)" "$rel"
  done < <(find "$root" -type f -print0 | LC_ALL=C sort -z)
done

unexpected_types="$(find /candidate/reference-semantics -mindepth 1 \
  ! -type d ! -type f -printf '%y %p -> %l\n')"
if [[ -n "$unexpected_types" ]]; then
  printf 'FAIL unexpected semantics entry types:\n%s\n' "$unexpected_types"
  failures=$((failures + 1))
else
  printf 'OK no symlink or special entries in candidate supplied semantics\n'
fi

for path in \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/verification.k \
  /candidate/spec.k \
  /candidate/prove.sh
do
  check_regular "$path"
done

printf 'PROVENANCE_FAILURE_COUNT=%s\n' "$failures"
exit "$failures"
