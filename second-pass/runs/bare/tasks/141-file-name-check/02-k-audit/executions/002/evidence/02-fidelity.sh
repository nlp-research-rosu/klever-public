#!/usr/bin/env bash
set -u

SCRATCH=/tmp/audit-work/141-file-name-check

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

run python3 "$SCRATCH/py2mpy.py" "$SCRATCH/solution.py"
python3 "$SCRATCH/py2mpy.py" "$SCRATCH/solution.py" \
  > "$SCRATCH/regenerated-solution.mpy"
printf '[translator redirection exit %d]\n' "$?"

run cmp -s "$SCRATCH/regenerated-solution.mpy" "$SCRATCH/solution.mpy"
run sha256sum "$SCRATCH/regenerated-solution.mpy" "$SCRATCH/solution.mpy"
run python3 /audit-output/evidence/02-differential.py
