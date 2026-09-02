#!/usr/bin/env bash
set -uo pipefail
set -x

status=0

for path in \
  /audit-input.json \
  /audit-campaign-lock.json \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt
do
  test -f "$path" && test ! -L "$path"
  rc=$?
  printf 'required_regular_file path=%s exit=%d\n' "$path" "$rc"
  (( rc == 0 )) || status=1
done

for path in \
  /candidate \
  /generation-evidence/codex-trace \
  /reference/reference-semantics
do
  test -d "$path" && test ! -L "$path"
  rc=$?
  printf 'required_real_directory path=%s exit=%d\n' "$path" "$rc"
  (( rc == 0 )) || status=1
done

sha256sum \
  /audit-campaign-lock.json \
  /run.json \
  /task.json \
  /generation-result.json \
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
  /generation-evidence/codex-trace/2026/07/23/rollout-2026-07-23T02-48-31-019f8df2-8e3c-72e2-b4e0-c36fade90602.jsonl

cmp -s /candidate/prompt.py /reference/prompt.py
rc=$?
printf 'candidate_prompt_byte_cmp_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

cmp -s /candidate/py2mpy.py /reference/py2mpy.py
rc=$?
printf 'candidate_translator_byte_cmp_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

diff -qr --no-dereference \
  /candidate/reference-semantics \
  /reference/reference-semantics
rc=$?
printf 'supplied_semantics_recursive_diff_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

links="$(find /candidate /reference /generation-evidence -type l -print)"
rc=$?
printf 'symlink_scan_exit=%d\n%s\n' "$rc" "$links"
(( rc == 0 )) || status=1
test -z "$links"
rc=$?
printf 'symlink_scan_empty_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

python3 -c '
import json
from pathlib import Path
a = json.loads(Path("/audit-input.json").read_text())
l = json.loads(Path("/audit-campaign-lock.json").read_text())
print("campaign_block_equals_lock=", a["audit_campaign"] == l)
print("record_layout=", a["record_layout"])
print("semantics_mode=", a["semantics_mode"])
assert a["audit_campaign"] == l
assert a["record_layout"] == "legacy-selected-stage1"
assert a["semantics_mode"] == "SUPPLIED_SEMANTICS"
'
rc=$?
printf 'campaign_and_mode_check_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

PYTHONPATH=/opt/humaneval/tools python3 -c '
from pathlib import Path
from pipeline_contract import sha256_tree
for label, path in (
    ("candidate_pipeline_tree", "/candidate"),
    ("candidate_semantics_manifest_tree", "/candidate/reference-semantics"),
    ("trusted_semantics_manifest_tree", "/reference/reference-semantics"),
    ("generation_trace_pipeline_tree", "/generation-evidence/codex-trace"),
):
    print(label, sha256_tree(Path(path)))
'
rc=$?
printf 'pipeline_tree_hash_check_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

find /candidate -type f -print0 |
  sort -z |
  xargs -0 sha256sum
rc=$?
printf 'candidate_per_file_hash_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

find /reference/reference-semantics -type f -print0 |
  sort -z |
  xargs -0 sha256sum
rc=$?
printf 'trusted_semantics_per_file_hash_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

python3 /audit-output/evidence/trace_summary.py
rc=$?
printf 'structured_trace_full_parse_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

printf 'stage1_integrity_exit=%d\n' "$status"
exit "$status"
