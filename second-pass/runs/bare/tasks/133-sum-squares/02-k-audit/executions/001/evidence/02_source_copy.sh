#!/usr/bin/env bash
set -u

log=/audit-output/evidence/02_source_copy.log
exec > >(tee "$log") 2>&1

scratch=/tmp/audit-work/133-sum-squares

run() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  return "$status"
}

run test ! -e "$scratch"
run mkdir -p "$scratch/trusted"
run cp \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/semantic.k \
  /candidate/verification.k \
  /candidate/spec.k \
  /candidate/prove.sh \
  "$scratch/"
run cp \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /reference/canonical.py \
  "$scratch/trusted/"
run find "$scratch" -maxdepth 2 -type f -printf '%P %s bytes\n'
run sha256sum \
  "$scratch/prompt.py" \
  "$scratch/py2mpy.py" \
  "$scratch/solution.py" \
  "$scratch/solution.mpy" \
  "$scratch/semantic.k" \
  "$scratch/verification.k" \
  "$scratch/spec.k" \
  "$scratch/prove.sh"
