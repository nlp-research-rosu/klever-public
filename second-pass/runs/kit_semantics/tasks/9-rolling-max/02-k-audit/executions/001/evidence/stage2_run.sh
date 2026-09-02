#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/rolling-max-20260729
log=/audit-output/evidence/stage2-fidelity-and-differential.log
: > "$log"

run_logged() {
  printf 'COMMAND:' >> "$log"
  printf ' %q' "$@" >> "$log"
  printf '\n' >> "$log"
  "$@" >> "$log" 2>&1
  local status=$?
  printf 'EXIT_STATUS: %s\n' "$status" >> "$log"
  return "$status"
}

printf 'COMMAND: python3 /reference/py2mpy.py %s/solution.py > %s/regenerated-solution.mpy\n' \
  "$scratch" "$scratch" >> "$log"
python3 /reference/py2mpy.py "$scratch/solution.py" \
  > "$scratch/regenerated-solution.mpy" 2>> "$log"
translator_status=$?
printf 'EXIT_STATUS: %s\n' "$translator_status" >> "$log"

run_logged cmp -s "$scratch/regenerated-solution.mpy" "$scratch/solution.mpy"
cmp_status=$?
run_logged sha256sum "$scratch/regenerated-solution.mpy" "$scratch/solution.mpy"
hash_status=$?
run_logged python3 /audit-output/evidence/differential_audit.py
differential_status=$?

if (( translator_status == 0 && cmp_status == 0 && hash_status == 0 && differential_status == 0 )); then
  printf 'STAGE2_OK=true\n' >> "$log"
  exit 0
fi
printf 'STAGE2_OK=false\n' >> "$log"
exit 1
