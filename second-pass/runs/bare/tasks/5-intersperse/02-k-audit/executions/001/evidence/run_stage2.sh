#!/usr/bin/env bash
set -u

log="/audit-output/evidence/stage2-fidelity.log"
scratch="/tmp/audit-work/reconstruction"
exec >"$log" 2>&1

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

run mkdir -p "$scratch"
run cp /reference/canonical.py "$scratch/canonical.py"
run cp /reference/prompt.py "$scratch/prompt.py"
run cp /reference/py2mpy.py "$scratch/py2mpy.py"
for source in solution.py solution.mpy semantic.k spec.k verification.k run-empty.mpy run-example.mpy; do
  run cp "/candidate/$source" "$scratch/$source"
done
run python3 "$scratch/py2mpy.py" "$scratch/solution.py"
run bash -c 'python3 /tmp/audit-work/reconstruction/py2mpy.py /tmp/audit-work/reconstruction/solution.py | cmp - /tmp/audit-work/reconstruction/solution.mpy'
run python3 /audit-output/evidence/differential_test.py
