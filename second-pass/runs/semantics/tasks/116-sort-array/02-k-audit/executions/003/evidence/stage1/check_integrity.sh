#!/usr/bin/env bash
set -u

audit_input=/audit-input.json
campaign_lock=/audit-campaign-lock.json

json_value() {
  python3 -c '
import json
import sys
value = json.load(open(sys.argv[1], encoding="utf-8"))
for component in sys.argv[2].split("."):
    value = value[component]
print(value)
' "$1" "$2"
}

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
  /generation-evidence/codex-last.txt
  /generation-evidence/codex-output.log
  /generation-evidence/prompt.txt
  /generation-evidence/codex-trace
)

overall=0
for required_path in "${required_paths[@]}"; do
  if [ -r "$required_path" ]; then
    printf 'READABLE %s\n' "$required_path"
  else
    printf 'MISSING_OR_UNREADABLE %s\n' "$required_path"
    overall=1
  fi
done

printf '\nDECLARED_LAYOUT %s\n' "$(json_value "$audit_input" record_layout)"
printf 'DECLARED_MODE %s\n' "$(json_value "$audit_input" semantics_mode)"

normalized_expected=$(mktemp)
normalized_actual=$(mktemp)
python3 -c 'import json,sys; print(json.dumps(json.load(open(sys.argv[1]))["audit_campaign"], sort_keys=True))' \
  "$audit_input" > "$normalized_expected"
python3 -c 'import json,sys; print(json.dumps(json.load(open(sys.argv[1])), sort_keys=True))' \
  "$campaign_lock" > "$normalized_actual"
if cmp -s "$normalized_expected" "$normalized_actual"; then
  echo 'CAMPAIGN_JSON_MATCH yes'
else
  echo 'CAMPAIGN_JSON_MATCH no'
  diff -u "$normalized_expected" "$normalized_actual"
  overall=1
fi
rm -f "$normalized_expected" "$normalized_actual"

check_file_hash() {
  local manifest_field=$1
  local mounted_path=$2
  local expected actual
  expected=$(json_value "$audit_input" "hashes.${manifest_field}")
  actual=$(sha256sum "$mounted_path" | cut -d' ' -f1)
  printf 'HASH %-45s expected=%s actual=%s match=%s\n' \
    "$mounted_path" "$expected" "$actual" "$([ "$expected" = "$actual" ] && echo yes || echo no)"
  if [ "$expected" != "$actual" ]; then
    overall=1
  fi
}

check_file_hash audit_campaign_lock_sha256 /audit-campaign-lock.json
check_file_hash canonical_sha256 /reference/canonical.py
check_file_hash trusted_prompt_sha256 /reference/prompt.py
check_file_hash trusted_translator_sha256 /reference/py2mpy.py
check_file_hash candidate_prompt_sha256 /candidate/prompt.py
check_file_hash candidate_translator_sha256 /candidate/py2mpy.py
check_file_hash run_manifest_sha256 /run.json
check_file_hash task_manifest_sha256 /task.json
check_file_hash stage1_result_sha256 /generation-result.json
check_file_hash stage1_invocation_sha256 /generation-evidence/invocation.json
check_file_hash generation_metrics_sha256 /generation-evidence/metrics.json
check_file_hash generation_usage_sha256 /generation-evidence/usage.json
check_file_hash generation_codex_last_sha256 /generation-evidence/codex-last.txt
check_file_hash generation_codex_output_sha256 /generation-evidence/codex-output.log
check_file_hash generation_prompt_sha256 /generation-evidence/prompt.txt

trace_expected=$(json_value "$audit_input" hashes.generation_codex_trace_sha256)
mapfile -t trace_files < <(find /generation-evidence/codex-trace -type f -print | LC_ALL=C sort)
if [ "${#trace_files[@]}" -eq 1 ]; then
  trace_actual=$(sha256sum "${trace_files[0]}" | cut -d' ' -f1)
  printf 'TRACE_SINGLE_FILE_HASH expected=%s actual=%s match=%s file=%s\n' \
    "$trace_expected" "$trace_actual" "$([ "$trace_expected" = "$trace_actual" ] && echo yes || echo no)" "${trace_files[0]}"
  if [ "$trace_expected" != "$trace_actual" ]; then
    echo 'TRACE_NOTE recorded value is a directory digest, not the sole file digest'
  fi
else
  printf 'TRACE_FILE_COUNT %d (directory hash convention must be checked separately)\n' "${#trace_files[@]}"
fi

for pair in \
  '/candidate/prompt.py /reference/prompt.py' \
  '/candidate/py2mpy.py /reference/py2mpy.py'
do
  read -r candidate_file trusted_file <<< "$pair"
  if cmp -s "$candidate_file" "$trusted_file"; then
    printf 'BYTE_IDENTICAL %s %s yes\n' "$candidate_file" "$trusted_file"
  else
    printf 'BYTE_IDENTICAL %s %s no\n' "$candidate_file" "$trusted_file"
    overall=1
  fi
done

if find /candidate/reference-semantics -type l -print -quit | grep -q .; then
  echo 'CANDIDATE_SEMANTICS_SYMLINKS yes'
  find /candidate/reference-semantics -type l -printf '%p -> %l\n'
  overall=1
else
  echo 'CANDIDATE_SEMANTICS_SYMLINKS no'
fi

if diff -r --no-dereference --brief /candidate/reference-semantics /reference/reference-semantics; then
  echo 'REFERENCE_SEMANTICS_RECURSIVE_MATCH yes'
else
  echo 'REFERENCE_SEMANTICS_RECURSIVE_MATCH no'
  diff -r --no-dereference /candidate/reference-semantics /reference/reference-semantics
  overall=1
fi

exit "$overall"
