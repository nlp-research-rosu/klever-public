#!/usr/bin/env bash
set -u
set -x

required=(
  /candidate/run-input.json
  /candidate/metrics.json
  /candidate/codex-last.txt
  /candidate/codex-output.log
  /candidate/prompt.py
  /candidate/py2mpy.py
  /candidate/solution.py
  /candidate/solution.mpy
  /candidate/spec.k
  /candidate/verification.k
)

test -d /reference/reference-semantics
reference_mount_status=$?

for artifact in "${required[@]}"; do
  stat --printf='%F %s %n\n' "$artifact"
done
required_status=$?

find /candidate -path /candidate/runtime-kompiled -prune \
  -o -path /candidate/verification-kompiled -prune \
  -o -type l -printf '%p -> %l\n'
candidate_symlink_scan_status=$?

find /reference -type l -printf '%p -> %l\n'
reference_symlink_scan_status=$?

cmp /candidate/prompt.py /reference/prompt.py
prompt_cmp_status=$?

cmp /candidate/py2mpy.py /reference/py2mpy.py
translator_cmp_status=$?

diff --recursive --brief --no-dereference \
  /candidate/reference-semantics /reference/reference-semantics
semantics_diff_status=$?

sha256sum \
  /candidate/prompt.py /reference/prompt.py \
  /candidate/py2mpy.py /reference/py2mpy.py

find /candidate/reference-semantics /reference/reference-semantics \
  -printf '%y %p -> %l\n' | sort

python3 -m json.tool /candidate/run-input.json
run_input_json_status=$?

python3 -m json.tool /candidate/metrics.json
metrics_json_status=$?

printf 'REFERENCE_MOUNT_STATUS=%d\n' "$reference_mount_status"
printf 'REQUIRED_STATUS=%d\n' "$required_status"
printf 'CANDIDATE_SYMLINK_SCAN_STATUS=%d\n' "$candidate_symlink_scan_status"
printf 'REFERENCE_SYMLINK_SCAN_STATUS=%d\n' "$reference_symlink_scan_status"
printf 'PROMPT_CMP_STATUS=%d\n' "$prompt_cmp_status"
printf 'TRANSLATOR_CMP_STATUS=%d\n' "$translator_cmp_status"
printf 'SEMANTICS_DIFF_STATUS=%d\n' "$semantics_diff_status"
printf 'RUN_INPUT_JSON_STATUS=%d\n' "$run_input_json_status"
printf 'METRICS_JSON_STATUS=%d\n' "$metrics_json_status"

if (( reference_mount_status != 0 || required_status != 0 ||
      prompt_cmp_status != 0 || translator_cmp_status != 0 ||
      semantics_diff_status != 0 || run_input_json_status != 0 ||
      metrics_json_status != 0 )); then
  exit 1
fi

exit 0
