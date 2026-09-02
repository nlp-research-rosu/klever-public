#!/usr/bin/env bash
set -u

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  return "$status"
}

run_capture() {
  output=$1
  shift
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf ' > %q\n' "$output"
  "$@" > "$output"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  return "$status"
}

run python3 /audit-output/evidence/provenance_check.py || exit $?

mkdir -p /tmp/audit-work/candidate /tmp/audit-work/reference
cp -a \
  /candidate/prompt.py \
  /candidate/prove.sh \
  /candidate/py2mpy.py \
  /candidate/semantic.k \
  /candidate/solution.mpy \
  /candidate/solution.py \
  /candidate/spec.k \
  /candidate/verification.k \
  /tmp/audit-work/candidate/
cp -a \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /tmp/audit-work/reference/

run_capture /tmp/audit-work/regenerated-solution.mpy \
  python3 /reference/py2mpy.py /tmp/audit-work/candidate/solution.py
run cmp -- /tmp/audit-work/regenerated-solution.mpy /tmp/audit-work/candidate/solution.mpy
run sha256sum \
  /tmp/audit-work/regenerated-solution.mpy \
  /tmp/audit-work/candidate/solution.mpy
run python3 /audit-output/evidence/differential_test.py
