#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT: %d\n' "$status"
  return "$status"
}

scratch=/tmp/audit-work/7-filter-by-substring/candidate
trusted=/tmp/audit-work/7-filter-by-substring/trusted

run python3 "$trusted/py2mpy.py" "$scratch/solution.py"
regen_status=$?
if [[ "$regen_status" -eq 0 ]]; then
  python3 "$trusted/py2mpy.py" "$scratch/solution.py" > "$scratch/solution.regenerated.mpy"
  printf 'REGENERATION_WRITE_EXIT: %d\n' "$?"
fi
run cmp "$scratch/solution.regenerated.mpy" "$scratch/solution.mpy"
run sha256sum "$scratch/solution.regenerated.mpy" "$scratch/solution.mpy"
run python3 /audit-output/evidence/02_differential.py
