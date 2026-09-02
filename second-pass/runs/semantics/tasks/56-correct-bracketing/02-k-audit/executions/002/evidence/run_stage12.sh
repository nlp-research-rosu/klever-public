#!/usr/bin/env bash
set -u

record() {
  name="$1"
  shift
  log="/audit-output/evidence/${name}.log"
  {
    printf 'COMMAND:'
    printf ' %q' "$@"
    printf '\n'
    "$@"
    status=$?
    printf 'EXIT_STATUS: %d\n' "$status"
    return "$status"
  } >"$log" 2>&1
}

record stage1_integrity python3 /audit-output/evidence/check_integrity.py
record stage1_trace_parse python3 /audit-output/evidence/inspect_trace.py

{
  printf 'COMMAND: python3 %q %q > %q\n' \
    /reference/py2mpy.py \
    /tmp/audit-work/reconstruction/solution.py \
    /tmp/audit-work/reconstruction/solution.regenerated.mpy
  python3 /reference/py2mpy.py \
    /tmp/audit-work/reconstruction/solution.py \
    > /tmp/audit-work/reconstruction/solution.regenerated.mpy
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
} > /audit-output/evidence/stage2_translate.log 2>&1

{
  printf 'COMMAND: cmp -s %q %q\n' \
    /tmp/audit-work/reconstruction/solution.regenerated.mpy \
    /tmp/audit-work/reconstruction/solution.submitted.mpy
  cmp -s \
    /tmp/audit-work/reconstruction/solution.regenerated.mpy \
    /tmp/audit-work/reconstruction/solution.submitted.mpy
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  sha256sum \
    /tmp/audit-work/reconstruction/solution.regenerated.mpy \
    /tmp/audit-work/reconstruction/solution.submitted.mpy
} > /audit-output/evidence/stage2_translation_identity.log 2>&1

record stage2_differential python3 /audit-output/evidence/differential_test.py
