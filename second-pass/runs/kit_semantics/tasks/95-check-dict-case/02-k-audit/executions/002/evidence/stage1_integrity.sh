#!/usr/bin/env bash
set -u

evidence_dir=/audit-output/evidence

required_paths=(
  /audit-input.json
  /audit-campaign-lock.json
  /candidate
  /reference/canonical.py
  /reference/prompt.py
  /reference/py2mpy.py
  /reference/reference-semantics
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
)

status=0
for path in "${required_paths[@]}"; do
  if [[ -r "$path" ]]; then
    stat -c 'REQUIRED_OK type=%F mode=%A path=%n' "$path"
  else
    printf 'REQUIRED_MISSING_OR_UNREADABLE path=%s\n' "$path"
    status=1
  fi
done

printf 'DIRECT_FILE_HASHES\n'
sha256sum \
  /audit-campaign-lock.json \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/runtime-metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt

python3 - <<'PY'
import hashlib
import json
from pathlib import Path

audit = json.loads(Path("/audit-input.json").read_text())
lock = json.loads(Path("/audit-campaign-lock.json").read_text())
print("CAMPAIGN_OBJECT_EQUALS_LOCK", audit["audit_campaign"] == lock)
print("RECORD_LAYOUT", audit["record_layout"])
print("SEMANTICS_MODE", audit["semantics_mode"])

expected = audit["hashes"]
checks = {
    "audit_campaign_lock_sha256": "/audit-campaign-lock.json",
    "canonical_sha256": "/reference/canonical.py",
    "trusted_prompt_sha256": "/reference/prompt.py",
    "trusted_translator_sha256": "/reference/py2mpy.py",
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
for key, path in checks.items():
    actual = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    print(
        "RECORDED_HASH_CHECK",
        key,
        "expected=" + expected[key],
        "actual=" + actual,
        "match=" + str(expected[key] == actual),
    )

stage1 = json.loads(Path("/generation-result.json").read_text())
for rel, recorded in sorted(stage1["outputs"]["evidence"].items()):
    path = Path("/generation-evidence") / rel
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    print(
        "STAGE1_EVIDENCE_HASH_CHECK",
        rel,
        "expected=" + recorded,
        "actual=" + actual,
        "match=" + str(recorded == actual),
    )
PY

cmp -s /candidate/prompt.py /reference/prompt.py
printf 'CANDIDATE_PROMPT_BYTE_IDENTICAL exit=%s\n' "$?"
cmp -s /candidate/py2mpy.py /reference/py2mpy.py
printf 'CANDIDATE_TRANSLATOR_BYTE_IDENTICAL exit=%s\n' "$?"

diff -qr --no-dereference \
  /reference/reference-semantics \
  /candidate/reference-semantics
semantics_diff_status=$?
printf 'SUPPLIED_SEMANTICS_RECURSIVE_DIFF exit=%s\n' "$semantics_diff_status"
if [[ "$semantics_diff_status" -ne 0 ]]; then
  status=1
fi

for root in \
  /candidate/reference-semantics \
  /reference/reference-semantics \
  /generation-evidence/codex-trace; do
  printf 'ENTRY_TYPE_COUNTS root=%s\n' "$root"
  find "$root" -printf '%y\n' | sort | uniq -c
  find "$root" -type l -printf 'SYMLINK path=%p target=%l\n'
done

(
  cd /candidate
  find . -type f -print0 |
    sort -z |
    xargs -0 sha256sum
) >"$evidence_dir/candidate-file-hashes.txt"

(
  cd /reference/reference-semantics
  find . -type f -print0 |
    sort -z |
    xargs -0 sha256sum
) >"$evidence_dir/trusted-semantics-file-hashes.txt"

(
  cd /candidate/reference-semantics
  find . -type f -print0 |
    sort -z |
    xargs -0 sha256sum
) >"$evidence_dir/candidate-semantics-file-hashes.txt"

cmp -s \
  "$evidence_dir/trusted-semantics-file-hashes.txt" \
  "$evidence_dir/candidate-semantics-file-hashes.txt"
printf 'SUPPLIED_SEMANTICS_HASH_MANIFEST_IDENTICAL exit=%s\n' "$?"

printf 'FINAL_STATUS %s\n' "$status"
exit "$status"
