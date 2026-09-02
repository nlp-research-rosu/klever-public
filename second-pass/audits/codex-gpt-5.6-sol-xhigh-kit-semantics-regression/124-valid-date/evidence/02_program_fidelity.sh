#!/usr/bin/env bash
set -u

record() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf 'EXIT_STATUS: %d\n\n' "$status"
  return "$status"
}

overall=0
work=/tmp/audit-work/124-valid-date

record python3 -m py_compile "$work/solution.py" "$work/trusted/canonical.py" || overall=1

printf 'COMMAND: python3 %q %q > %q\n' \
  "$work/trusted/py2mpy.py" "$work/solution.py" "$work/solution.regenerated.mpy"
python3 "$work/trusted/py2mpy.py" "$work/solution.py" \
  > "$work/solution.regenerated.mpy"
status=$?
printf 'EXIT_STATUS: %d\n\n' "$status"
if (( status != 0 )); then
  overall=1
fi

record cmp "$work/solution.regenerated.mpy" "$work/solution.mpy" || overall=1
record sha256sum "$work/solution.regenerated.mpy" "$work/solution.mpy" || overall=1

record env PYTHONDONTWRITEBYTECODE=1 python3 \
  /audit-output/evidence/02_differential.py \
  --canonical "$work/trusted/canonical.py" \
  --candidate "$work/solution.py" \
  --write-inputs /audit-output/evidence/02_differential-inputs.json \
  || overall=1

printf 'OVERALL_STATUS: %d\n' "$overall"
exit "$overall"
