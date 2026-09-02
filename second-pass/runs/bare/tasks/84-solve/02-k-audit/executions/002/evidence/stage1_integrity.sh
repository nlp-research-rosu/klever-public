#!/usr/bin/env bash
set -uo pipefail

required=(
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
)

status=0
for path in "${required[@]}"; do
  if [[ -f "$path" && ! -L "$path" && -r "$path" ]]; then
    printf 'REGULAR_READABLE %s\n' "$path"
  else
    printf 'BAD_REQUIRED_TYPE %s\n' "$path"
    status=1
  fi
done

trace_files=0
while IFS= read -r -d '' path; do
  trace_files=$((trace_files + 1))
  if [[ ! -f "$path" || -L "$path" || ! -r "$path" ]]; then
    printf 'BAD_TRACE_TYPE %s\n' "$path"
    status=1
  fi
done < <(find /generation-evidence/codex-trace -type f -print0)
printf 'TRACE_REGULAR_FILE_COUNT %d\n' "$trace_files"
if [[ "$trace_files" -eq 0 ]]; then
  status=1
fi

if find /candidate /generation-evidence /reference -type l -print -quit | grep -q .; then
  printf 'SYMLINK_FOUND\n'
  find /candidate /generation-evidence /reference -type l -print
  status=1
else
  printf 'NO_SYMLINKS candidate generation-evidence reference\n'
fi

if [[ -e /reference/reference-semantics || -L /reference/reference-semantics ]]; then
  printf 'BAD_GENERATED_MODE_REFERENCE_SEMANTICS_PRESENT\n'
  status=1
else
  printf 'GENERATED_MODE_REFERENCE_SEMANTICS_ABSENT\n'
fi

cmp -s /candidate/prompt.py /reference/prompt.py
prompt_cmp=$?
cmp -s /candidate/py2mpy.py /reference/py2mpy.py
translator_cmp=$?
printf 'PROMPT_BYTE_CMP_EXIT %d\n' "$prompt_cmp"
printf 'TRANSLATOR_BYTE_CMP_EXIT %d\n' "$translator_cmp"
if [[ "$prompt_cmp" -ne 0 || "$translator_cmp" -ne 0 ]]; then
  status=1
fi

printf 'SHA256_REGULAR_INPUTS\n'
sha256sum \
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

printf 'SHA256_TRACE_FILES\n'
find /generation-evidence/codex-trace -type f -print0 |
  sort -z |
  xargs -0 sha256sum

printf 'REVIEWER_CANDIDATE_FILESET_DIGEST\n'
find /candidate -type f -print0 |
  sort -z |
  xargs -0 sha256sum |
  sha256sum

printf 'REVIEWER_TRACE_FILESET_DIGEST\n'
find /generation-evidence/codex-trace -type f -print0 |
  sort -z |
  xargs -0 sha256sum |
  sha256sum

python3 - <<'PY'
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, "/opt/humaneval/tools")
from pipeline_contract import sha256_tree

audit = json.loads(Path("/audit-input.json").read_text())
lock_bytes = Path("/audit-campaign-lock.json").read_bytes()
lock = json.loads(lock_bytes)
generation_result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads(
    Path("/generation-evidence/invocation.json").read_text()
)
usage = json.loads(Path("/generation-evidence/usage.json").read_text())
candidate_pipeline_digest = sha256_tree(Path("/candidate"))
trace_pipeline_digest = sha256_tree(
    Path("/generation-evidence/codex-trace")
)

checks = {
    "campaign_block_equal": lock == audit["audit_campaign"],
    "campaign_lock_hash_equal": (
        hashlib.sha256(lock_bytes).hexdigest()
        == audit["hashes"]["audit_campaign_lock_sha256"]
    ),
    "record_layout_legacy_selected_stage1": (
        audit["record_layout"] == "legacy-selected-stage1"
    ),
    "semantics_mode_generated": audit["semantics_mode"] == "GENERATED_SEMANTICS",
    "problem_id_84_solve": audit["problem_id"] == "84-solve",
    "condition_bare": audit["condition"] == "bare",
    "candidate_matches_generation_workspace": (
        candidate_pipeline_digest
        == generation_result["outputs"]["workspace_sha256"]
        == invocation["retained_workspace_sha256"]
    ),
    "trace_matches_usage_source_trace": (
        trace_pipeline_digest == usage["source_trace_sha256"]
    ),
}

print(f"candidate_pipeline_tree_sha256={candidate_pipeline_digest}")
print(f"trace_pipeline_tree_sha256={trace_pipeline_digest}")
for name, passed in checks.items():
    print(f"{name}={str(passed).lower()}")

for path in (
    "/audit-input.json",
    "/audit-campaign-lock.json",
    "/run.json",
    "/task.json",
    "/generation-result.json",
    "/generation-evidence/invocation.json",
    "/generation-evidence/metrics.json",
    "/generation-evidence/usage.json",
):
    json.loads(Path(path).read_text())
    print(f"JSON_VALID {path}")

if not all(checks.values()):
    raise SystemExit(1)
PY
python_status=$?
if [[ "$python_status" -ne 0 ]]; then
  status=1
fi

printf 'OVERALL_EXIT %d\n' "$status"
exit "$status"
