#!/usr/bin/env bash
set -uo pipefail

SCRATCH=/tmp/audit-work/90-next-smallest

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

run mkdir -p "$SCRATCH/source"
run cp -p \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/semantic.k \
  /candidate/verification.k \
  /candidate/spec.k \
  "$SCRATCH/source/"
run cp -p /reference/canonical.py /reference/prompt.py /reference/py2mpy.py \
  "$SCRATCH/source/"

printf '$ python3 /reference/py2mpy.py /candidate/solution.py > %s\n' \
  "$SCRATCH/source/solution.regenerated.mpy"
python3 /reference/py2mpy.py /candidate/solution.py \
  > "$SCRATCH/source/solution.regenerated.mpy"
status=$?
printf '[exit %d]\n' "$status"

run cmp "$SCRATCH/source/solution.regenerated.mpy" /candidate/solution.mpy
run sha256sum \
  "$SCRATCH/source/solution.regenerated.mpy" \
  /candidate/solution.mpy
run python3 -m py_compile "$SCRATCH/source/solution.py"

printf 'Scratch source inventory (candidate compiled definitions/caches were not copied):\n'
run find "$SCRATCH/source" -maxdepth 1 -printf '%y %f %s bytes\n'
