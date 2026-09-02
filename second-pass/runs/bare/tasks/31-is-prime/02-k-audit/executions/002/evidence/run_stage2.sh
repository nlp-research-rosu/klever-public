#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/review-31
candidate="$scratch/candidate"
reference="$scratch/reference"

printf 'COMMAND: python3 %s %s > %s\n' \
  "$reference/py2mpy.py" "$candidate/solution.py" "$scratch/regenerated.mpy"
python3 "$reference/py2mpy.py" "$candidate/solution.py" > "$scratch/regenerated.mpy"
translate_rc=$?
printf 'EXIT: %d\n' "$translate_rc"

printf 'COMMAND: cmp -s %s %s\n' \
  "$scratch/regenerated.mpy" "$candidate/solution.mpy"
cmp -s "$scratch/regenerated.mpy" "$candidate/solution.mpy"
cmp_rc=$?
printf 'EXIT: %d\n' "$cmp_rc"
if [[ "$cmp_rc" -ne 0 ]]; then
  diff -u "$candidate/solution.mpy" "$scratch/regenerated.mpy" || true
fi

printf 'COMMAND: PYTHONDONTWRITEBYTECODE=1 python3 %s %s %s\n' \
  /audit-output/evidence/differential.py \
  "$reference/canonical.py" "$candidate/solution.py"
PYTHONDONTWRITEBYTECODE=1 python3 \
  /audit-output/evidence/differential.py \
  "$reference/canonical.py" \
  "$candidate/solution.py"
diff_rc=$?
printf 'EXIT: %d\n' "$diff_rc"

if [[ "$translate_rc" -ne 0 || "$cmp_rc" -ne 0 ]]; then
  exit 2
fi
exit "$diff_rc"
