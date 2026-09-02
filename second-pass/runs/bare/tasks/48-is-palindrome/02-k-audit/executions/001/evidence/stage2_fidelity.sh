#!/usr/bin/env bash
set -uo pipefail

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@" 2>&1
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

scratch=/tmp/audit-work/48-is-palindrome
mkdir -p "$scratch/source" "$scratch/trusted"

for artifact in \
  solution.py solution.mpy semantic.k verification.k spec.k prove.sh prompt.py py2mpy.py
do
  run cp -p "/candidate/$artifact" "$scratch/source/$artifact" || exit $?
done

for artifact in canonical.py prompt.py py2mpy.py
do
  run cp -p "/reference/$artifact" "$scratch/trusted/$artifact" || exit $?
done

printf '$ python3 %q %q > %q\n' \
  "$scratch/trusted/py2mpy.py" \
  "$scratch/source/solution.py" \
  "$scratch/regenerated-solution.mpy"
python3 "$scratch/trusted/py2mpy.py" "$scratch/source/solution.py" \
  > "$scratch/regenerated-solution.mpy" 2> "$scratch/regenerate.stderr"
status=$?
sed -n '1,120p' "$scratch/regenerate.stderr"
printf '[exit %d]\n' "$status"
test "$status" -eq 0 || exit "$status"

run cmp -s "$scratch/regenerated-solution.mpy" "$scratch/source/solution.mpy" \
  || exit $?
run sha256sum "$scratch/regenerated-solution.mpy" "$scratch/source/solution.mpy" \
  || exit $?
run python3 /audit-output/evidence/differential_test.py \
  --canonical "$scratch/trusted/canonical.py" \
  --solution "$scratch/source/solution.py" \
  --inputs-out /audit-output/evidence/differential_inputs.jsonl \
  || exit $?
run wc -l /audit-output/evidence/differential_inputs.jsonl || exit $?
run sha256sum /audit-output/evidence/differential_inputs.jsonl || exit $?
