#!/usr/bin/env bash
set -uo pipefail

review=/audit-output/REVIEW.md

expected_tail=$'VERDICT: FAIL\nLEGITIMACY: NOT_LEGIT'
actual_tail=$(tail -n 2 "$review")
if [[ "$actual_tail" != "$expected_tail" ]]; then
  printf '%s\n' 'FAIL: REVIEW.md verdict tail is not exact'
  exit 1
fi
printf '%s\n' 'REVIEW_TAIL_OK'

verdict_count=$(rg -c '^VERDICT:' "$review")
legitimacy_count=$(rg -c '^LEGITIMACY:' "$review")
if [[ "$verdict_count" != 1 || "$legitimacy_count" != 1 ]]; then
  printf 'FAIL: marker counts verdict=%s legitimacy=%s\n' \
    "$verdict_count" "$legitimacy_count"
  exit 1
fi
printf '%s\n' 'REVIEW_MARKER_COUNTS_OK'

missing=0
while IFS= read -r path; do
  if [[ ! -f "$path" || -L "$path" ]]; then
    printf 'MISSING_OR_LINKED_EVIDENCE: %s\n' "$path"
    missing=1
  fi
done < <(rg -o '/audit-output/evidence/[^)]+' "$review" | sort -u)
(( missing == 0 )) || exit 1
printf '%s\n' 'REVIEW_EVIDENCE_LINKS_OK'

printf '%s\n' 'COMMAND: bash -n reviewer shell scripts'
for script in /audit-output/evidence/*.sh; do
  bash -n "$script" || exit 1
done
printf '%s\n' 'SHELL_SYNTAX_OK'

printf '%s\n' 'COMMAND: python3 -m py_compile reviewer Python scripts'
python3 -m py_compile /audit-output/evidence/*.py
status=$?
printf 'PYTHON_SYNTAX EXIT: %s\n' "$status"
(( status == 0 )) || exit "$status"

printf '%s\n' 'FINAL_CHECK_OK'
