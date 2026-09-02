#!/usr/bin/env bash
set -uo pipefail
set -x

overall=0

printf '%s\n' 'REQUIRED ARTIFACT LSTAT'
for path in \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/spec.k \
  /candidate/verification.k \
  /candidate/codex-trace; do
  stat -c 'type=%F mode=%A size=%s path=%n' "$path"
  status=$?
  printf 'lstat_status=%s path=%s\n' "$status" "$path"
  if (( status != 0 )); then
    overall=1
  fi
done

printf '%s\n' 'ALL CANDIDATE SYMLINKS'
find /candidate -type l -printf '%p -> %l\n'
symlink_count=$(find /candidate -type l -print | wc -l)
printf 'candidate_symlink_count=%s\n' "$symlink_count"
if (( symlink_count != 0 )); then
  overall=1
fi

sha256sum \
  /reference/prompt.py \
  /candidate/prompt.py \
  /reference/py2mpy.py \
  /candidate/py2mpy.py \
  /reference/canonical.py \
  /candidate/solution.py \
  /candidate/solution.mpy

printf '%s\n' 'UNTRUSTED CLAIM FILE SIZES'
wc -l -c \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log \
  /candidate/codex-trace/2026/07/22/*.jsonl

printf '%s\n' 'UNTRUSTED FINAL CLAIM'
sed -n '1,80p' /candidate/codex-last.txt

printf 'STAGE1_SUPPLEMENT_OVERALL=%s\n' "$overall"
exit "$overall"
