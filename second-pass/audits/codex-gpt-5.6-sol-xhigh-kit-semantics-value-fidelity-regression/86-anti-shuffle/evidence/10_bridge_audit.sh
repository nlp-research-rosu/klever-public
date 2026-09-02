#!/usr/bin/env bash
set -u

SCRATCH=/tmp/audit-work/anti-shuffle-audit
EVIDENCE=/audit-output/evidence
overall=0

run_logged() {
  output=$1
  shift
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@" > "$output" 2>&1
  status=$?
  printf 'EXIT: %d\n' "$status"
  printf 'OUTPUT: %s\n\n' "$output"
  if [ "$status" -ne 0 ]; then
    overall=1
  fi
}

run_logged "$EVIDENCE/10_bridge_python.log" \
  python3 "$EVIDENCE/10_bridge_harness.py"

printf 'COMMAND: python3 %q %q > %q\n' \
  /reference/py2mpy.py "$EVIDENCE/10_bridge_harness.py" "$SCRATCH/10_bridge_harness.mpy"
python3 /reference/py2mpy.py "$EVIDENCE/10_bridge_harness.py" \
  > "$SCRATCH/10_bridge_harness.mpy" \
  2> "$EVIDENCE/10_bridge_translate.stderr"
status=$?
printf 'EXIT: %d\n\n' "$status"
if [ "$status" -ne 0 ]; then
  overall=1
fi

run_logged "$EVIDENCE/10_bridge_fixed.log" \
  krun "$SCRATCH/10_bridge_harness.mpy" \
  --definition "$SCRATCH/runtime-kompiled"
run_logged "$EVIDENCE/10_bridge_extended.log" \
  krun "$SCRATCH/10_bridge_harness.mpy" \
  --definition "$SCRATCH/verification-kompiled"

printf 'COMMAND: cmp -s %q %q\n' \
  "$EVIDENCE/10_bridge_fixed.log" "$EVIDENCE/10_bridge_extended.log"
cmp -s "$EVIDENCE/10_bridge_fixed.log" "$EVIDENCE/10_bridge_extended.log"
status=$?
printf 'EXIT: %d\n\n' "$status"
if [ "$status" -ne 0 ]; then
  overall=1
fi

run_logged "$EVIDENCE/10_bridge_symbolic.log" \
  kprove "$EVIDENCE/10_bridge_symbolic.k" \
  --definition "$SCRATCH/verification-kompiled" \
  --spec-module AUDIT-BRIDGE-SYMBOLIC

exit "$overall"
