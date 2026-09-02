#!/usr/bin/env bash
set -u

SCRATCH=/tmp/audit-work/anti-shuffle-audit
printf 'COMMAND: cd %q && python3 %q %q > %q\n' \
  "$SCRATCH" /reference/py2mpy.py solution.py solution.regenerated.mpy
(
  cd "$SCRATCH" || exit 1
  python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy
)
status=$?
printf 'EXIT: %d\n\n' "$status"

printf 'COMMAND: cmp -s %q %q\n' \
  "$SCRATCH/solution.regenerated.mpy" "$SCRATCH/solution.submitted.mpy"
cmp -s "$SCRATCH/solution.regenerated.mpy" "$SCRATCH/solution.submitted.mpy"
status=$?
printf 'EXIT: %d\n\n' "$status"

printf 'COMMAND: sha256sum %q %q\n' \
  "$SCRATCH/solution.regenerated.mpy" "$SCRATCH/solution.submitted.mpy"
sha256sum "$SCRATCH/solution.regenerated.mpy" "$SCRATCH/solution.submitted.mpy"
status=$?
printf 'EXIT: %d\n' "$status"
