#!/usr/bin/env bash
set -u

log=/audit-output/evidence/02_prepare_scratch.log
exec > >(tee "$log") 2>&1

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  if test "$status" -ne 0; then
    exit "$status"
  fi
}

scratch=/tmp/audit-work/rebuild
run rm -rf -- "$scratch"
run mkdir -p "$scratch/candidate" "$scratch/trusted"
run cp -a /candidate/reference-semantics "$scratch/candidate/reference-semantics"
run cp /candidate/solution.py /candidate/solution.mpy \
  /candidate/spec.k /candidate/verification.k "$scratch/candidate/"
run cp /reference/canonical.py /reference/prompt.py /reference/py2mpy.py \
  "$scratch/trusted/"
run find "$scratch" -maxdepth 4 -printf '%y %p -> %l\n'
