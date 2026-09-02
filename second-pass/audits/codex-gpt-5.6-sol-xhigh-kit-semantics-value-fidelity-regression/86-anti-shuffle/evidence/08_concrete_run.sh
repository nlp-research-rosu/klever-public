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

run_logged "$EVIDENCE/08_harness_identity.log" \
  python3 "$EVIDENCE/08_check_harness_identity.py"
run_logged "$EVIDENCE/08_harness_python.log" \
  python3 "$EVIDENCE/08_concrete_harness.py"

printf 'COMMAND: python3 %q %q > %q\n' \
  /reference/py2mpy.py "$EVIDENCE/08_concrete_harness.py" "$SCRATCH/08_concrete_harness.mpy"
python3 /reference/py2mpy.py "$EVIDENCE/08_concrete_harness.py" \
  > "$SCRATCH/08_concrete_harness.mpy" \
  2> "$EVIDENCE/08_translate_harness.stderr"
status=$?
printf 'EXIT: %d\n' "$status"
printf 'STDERR: %s\n\n' "$EVIDENCE/08_translate_harness.stderr"
if [ "$status" -ne 0 ]; then
  overall=1
fi

run_logged "$EVIDENCE/08_krun_fixed.log" \
  krun "$SCRATCH/08_concrete_harness.mpy" \
  --definition "$SCRATCH/runtime-kompiled"

exit "$overall"
