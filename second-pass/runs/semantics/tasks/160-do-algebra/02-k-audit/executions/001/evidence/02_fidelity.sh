#!/usr/bin/env bash
set -u

LOG=/audit-output/evidence/02_fidelity.log
: > "$LOG"

run() {
  printf 'COMMAND: ' >> "$LOG"
  printf '%q ' "$@" >> "$LOG"
  printf '\n' >> "$LOG"
  "$@" >> "$LOG" 2>&1
  status=$?
  printf 'EXIT: %d\n\n' "$status" >> "$LOG"
  return 0
}

run mkdir -p /tmp/audit-work/rebuild
run cp /candidate/solution.py /tmp/audit-work/rebuild/solution.py
run cp /candidate/solution.mpy /tmp/audit-work/rebuild/solution.mpy
run cp /candidate/spec.k /tmp/audit-work/rebuild/spec.k
run cp /candidate/verification.k /tmp/audit-work/rebuild/verification.k
run cp /candidate/prove.sh /tmp/audit-work/rebuild/prove.sh
run cp -a /candidate/reference-semantics /tmp/audit-work/rebuild/reference-semantics
run cp /reference/canonical.py /tmp/audit-work/rebuild/canonical.py
run cp /reference/prompt.py /tmp/audit-work/rebuild/trusted-prompt.py
run cp /reference/py2mpy.py /tmp/audit-work/rebuild/trusted-py2mpy.py

printf 'COMMAND: python3 /reference/py2mpy.py /candidate/solution.py > /tmp/audit-work/rebuild/regenerated-solution.mpy\n' >> "$LOG"
python3 /reference/py2mpy.py /candidate/solution.py > /tmp/audit-work/rebuild/regenerated-solution.mpy 2>> "$LOG"
status=$?
printf 'EXIT: %d\n\n' "$status" >> "$LOG"

run cmp -s /candidate/solution.mpy /tmp/audit-work/rebuild/regenerated-solution.mpy
run sha256sum /candidate/solution.mpy /tmp/audit-work/rebuild/regenerated-solution.mpy
run python3 /audit-output/evidence/02_differential.py \
  --canonical /reference/canonical.py \
  --candidate /candidate/solution.py \
  --results /audit-output/evidence/02_differential-results.json
