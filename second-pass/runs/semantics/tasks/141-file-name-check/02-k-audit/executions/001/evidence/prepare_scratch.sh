#!/usr/bin/env bash
set -uo pipefail

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

scratch=/tmp/audit-work/141-file-name-check
run mkdir -p "$scratch"
run cp /candidate/solution.py "$scratch/solution.py"
run cp /candidate/solution.mpy "$scratch/submitted-solution.mpy"
run cp /candidate/spec.k "$scratch/spec.k"
run cp /candidate/verification.k "$scratch/verification.k"
run cp /reference/canonical.py "$scratch/canonical.py"
run cp /reference/prompt.py "$scratch/prompt.py"
run cp /reference/py2mpy.py "$scratch/py2mpy.py"
run cp -a /reference/reference-semantics "$scratch/reference-semantics"
run find "$scratch" -type l -print
run find "$scratch" -maxdepth 3 -type f -printf '%P\n'
