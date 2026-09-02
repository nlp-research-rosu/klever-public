#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/proof-162

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

run mkdir -p "$scratch"
run cp -a /reference/reference-semantics "$scratch/reference-semantics"
run cp -a /reference/canonical.py "$scratch/canonical.py"
run cp -a /reference/prompt.py "$scratch/prompt.py"
run cp -a /reference/py2mpy.py "$scratch/py2mpy.py"
run cp -a /candidate/solution.py "$scratch/solution.py"
run cp -a /candidate/solution.mpy "$scratch/solution.submitted.mpy"
run cp -a /candidate/verification.k "$scratch/verification.k"
run cp -a /candidate/spec.k "$scratch/spec.k"
run find "$scratch" -type l -print
run find "$scratch" -maxdepth 2 -type f -printf '%P %s bytes\n'
