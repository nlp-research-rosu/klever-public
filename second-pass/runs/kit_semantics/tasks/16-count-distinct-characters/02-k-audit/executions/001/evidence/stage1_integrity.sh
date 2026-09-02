#!/usr/bin/env bash
set -u
set -o pipefail

exec > >(tee /audit-output/evidence/stage1_integrity.log) 2>&1
set -x

sha256sum \
  /audit-campaign-lock.json \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
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
  /generation-evidence/codex-trace/2026/07/29/rollout-2026-07-29T08-50-49-019fae24-682c-7cc0-b9fe-08e8acabae7a.jsonl
hash_status=$?
printf 'sha256sum_exit=%d\n' "$hash_status"

cmp -s /candidate/prompt.py /reference/prompt.py
prompt_cmp_status=$?
printf 'candidate_prompt_cmp_exit=%d\n' "$prompt_cmp_status"

cmp -s /candidate/py2mpy.py /reference/py2mpy.py
translator_cmp_status=$?
printf 'candidate_translator_cmp_exit=%d\n' "$translator_cmp_status"

find /candidate/reference-semantics -mindepth 1 -printf '%P\t%y\t%l\n' |
  LC_ALL=C sort > /audit-output/evidence/candidate-semantics-entries.txt
candidate_entries_status=$?
printf 'candidate_semantics_entries_exit=%d\n' "$candidate_entries_status"

find /reference/reference-semantics -mindepth 1 -printf '%P\t%y\t%l\n' |
  LC_ALL=C sort > /audit-output/evidence/trusted-semantics-entries.txt
trusted_entries_status=$?
printf 'trusted_semantics_entries_exit=%d\n' "$trusted_entries_status"

diff -u \
  /audit-output/evidence/trusted-semantics-entries.txt \
  /audit-output/evidence/candidate-semantics-entries.txt
entry_diff_status=$?
printf 'semantics_entry_diff_exit=%d\n' "$entry_diff_status"

find /candidate/reference-semantics -type l -print
candidate_symlink_status=$?
printf 'candidate_semantics_symlink_scan_exit=%d\n' "$candidate_symlink_status"

(
  cd /candidate/reference-semantics || exit 1
  find . -type f -print0 |
    LC_ALL=C sort -z |
    xargs -0 sha256sum
) > /audit-output/evidence/candidate-semantics-file-hashes.txt
candidate_hash_status=$?
printf 'candidate_semantics_file_hash_exit=%d\n' "$candidate_hash_status"

(
  cd /reference/reference-semantics || exit 1
  find . -type f -print0 |
    LC_ALL=C sort -z |
    xargs -0 sha256sum
) > /audit-output/evidence/trusted-semantics-file-hashes.txt
trusted_hash_status=$?
printf 'trusted_semantics_file_hash_exit=%d\n' "$trusted_hash_status"

diff -u \
  /audit-output/evidence/trusted-semantics-file-hashes.txt \
  /audit-output/evidence/candidate-semantics-file-hashes.txt
hash_diff_status=$?
printf 'semantics_file_hash_diff_exit=%d\n' "$hash_diff_status"

sha256sum \
  /audit-output/evidence/candidate-semantics-entries.txt \
  /audit-output/evidence/candidate-semantics-file-hashes.txt \
  /audit-output/evidence/trusted-semantics-entries.txt \
  /audit-output/evidence/trusted-semantics-file-hashes.txt
aggregate_status=$?
printf 'reviewer_manifest_hash_exit=%d\n' "$aggregate_status"

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

required_status=0
for required_path in "${required_paths[@]}"; do
  if [[ ! -r "$required_path" ]]; then
    printf 'MISSING_OR_UNREADABLE %s\n' "$required_path"
    required_status=1
  fi
done
printf 'required_path_check_exit=%d\n' "$required_status"

find \
  /audit-input.json \
  /audit-campaign-lock.json \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence \
  /reference \
  -type l -print
provenance_symlink_status=$?
printf 'provenance_symlink_scan_exit=%d\n' "$provenance_symlink_status"

exit "$required_status"
