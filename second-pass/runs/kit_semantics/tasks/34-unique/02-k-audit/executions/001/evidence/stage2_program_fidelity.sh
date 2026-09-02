#!/usr/bin/env bash
set -uo pipefail

log=/audit-output/evidence/stage2_program_fidelity.log
scratch=/tmp/audit-work/review-34-unique
exec >"$log" 2>&1

run() {
  echo "COMMAND: $*"
  "$@"
  status=$?
  echo "EXIT: $status"
  return "$status"
}

echo "STAGE 2 PROGRAM FIDELITY AND DIFFERENTIAL"
run sha256sum "$scratch/solution.py" "$scratch/solution.mpy" "$scratch/py2mpy.py"

echo "COMMAND: python3 $scratch/py2mpy.py $scratch/solution.py > $scratch/regenerated-solution.mpy"
python3 "$scratch/py2mpy.py" "$scratch/solution.py" > "$scratch/regenerated-solution.mpy"
status=$?
echo "EXIT: $status"

run cmp "$scratch/solution.mpy" "$scratch/regenerated-solution.mpy"
run sha256sum "$scratch/solution.mpy" "$scratch/regenerated-solution.mpy"
run python3 /audit-output/evidence/independent_differential.py
