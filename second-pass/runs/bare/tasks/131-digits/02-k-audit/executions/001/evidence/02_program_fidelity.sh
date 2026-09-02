#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/131-digits

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

printf 'AUDIT STAGE 2: PROGRAM FIDELITY AND DIFFERENTIAL TESTING\n'

run mkdir -p "$scratch/trusted"
run cp /candidate/solution.py "$scratch/solution.py"
run cp /candidate/solution.mpy "$scratch/solution.mpy"
run cp /candidate/semantic.k "$scratch/semantic.k"
run cp /candidate/verification.k "$scratch/verification.k"
run cp /candidate/spec.k "$scratch/spec.k"
run cp /candidate/prove.sh "$scratch/prove.sh"
run cp /candidate/prompt.py "$scratch/prompt.py"
run cp /candidate/py2mpy.py "$scratch/py2mpy.py"
run cp /reference/canonical.py "$scratch/trusted/canonical.py"
run cp /reference/prompt.py "$scratch/trusted/prompt.py"
run cp /reference/py2mpy.py "$scratch/trusted/py2mpy.py"

printf '\n$ python3 /reference/py2mpy.py %q > %q\n' \
  "$scratch/solution.py" "$scratch/solution.regenerated.mpy"
python3 /reference/py2mpy.py "$scratch/solution.py" \
  > "$scratch/solution.regenerated.mpy"
status=$?
printf '[exit %d]\n' "$status"

run sha256sum "$scratch/solution.mpy" "$scratch/solution.regenerated.mpy"
run cmp -s "$scratch/solution.mpy" "$scratch/solution.regenerated.mpy"
run cp "$scratch/solution.regenerated.mpy" \
  /audit-output/evidence/02_solution_regenerated.mpy

printf '\nTrusted prompt:\n'
run sed -n 1,120p /reference/prompt.py
printf '\nTrusted canonical implementation:\n'
run sed -n 1,160p /reference/canonical.py
printf '\nGenerated Python implementation:\n'
run sed -n 1,160p "$scratch/solution.py"
printf '\nRegenerated constructor tree:\n'
run sed -n 1,240p "$scratch/solution.regenerated.mpy"

run python3 /audit-output/evidence/02_differential.py
