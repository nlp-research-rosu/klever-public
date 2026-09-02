#!/usr/bin/env bash
set -u

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT: %d\n\n' "$status"
  return "$status"
}

SCRATCH=/tmp/audit-work/anti-shuffle-audit
run mkdir -p "$SCRATCH"
run cp /candidate/solution.py "$SCRATCH/solution.py"
run cp /candidate/solution.mpy "$SCRATCH/solution.submitted.mpy"
run cp /candidate/spec.k "$SCRATCH/spec.k"
run cp /candidate/verification.k "$SCRATCH/verification.k"
run cp /reference/canonical.py "$SCRATCH/canonical.py"
run cp /reference/prompt.py "$SCRATCH/prompt.py"
run cp /reference/py2mpy.py "$SCRATCH/py2mpy.py"
run cp -a /reference/reference-semantics "$SCRATCH/reference-semantics"
run find "$SCRATCH" -maxdepth 3 -printf '%y %p -> %l\n'
