#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/candidate || exit 99
overall=0

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %s\n' "$status"
  if (( status != 0 )); then
    overall=1
  fi
}

run cp /audit-output/evidence/runtime_witness.py \
  /tmp/audit-work/candidate/runtime_witness.py
run cp /audit-output/evidence/runtime_witness_expect_false.py \
  /tmp/audit-work/candidate/runtime_witness_expect_false.py
run cp /audit-output/evidence/runtime_witness_expect_true.py \
  /tmp/audit-work/candidate/runtime_witness_expect_true.py

printf '%s\n' 'COMMAND: python3 /tmp/audit-work/trusted/py2mpy.py runtime_witness.py > runtime_witness.mpy'
python3 /tmp/audit-work/trusted/py2mpy.py \
  runtime_witness.py \
  > runtime_witness.mpy
status=$?
printf 'EXIT_STATUS: %s\n' "$status"
if (( status != 0 )); then
  overall=1
fi

for expectation in false true; do
  printf 'COMMAND: python3 /tmp/audit-work/trusted/py2mpy.py runtime_witness_expect_%s.py > runtime_witness_expect_%s.mpy\n' \
    "$expectation" "$expectation"
  python3 /tmp/audit-work/trusted/py2mpy.py \
    "runtime_witness_expect_${expectation}.py" \
    > "runtime_witness_expect_${expectation}.mpy"
  status=$?
  printf 'EXIT_STATUS: %s\n' "$status"
  if (( status != 0 )); then
    overall=1
  fi
done

run python3 -c \
  'import runtime_witness as w; print(w.iscube(1000000000000000000000000000000000000000000000))'
run krun runtime_witness.mpy \
  --definition runtime-audit-kompiled \
  --output pretty
run krun runtime_witness_expect_false.mpy \
  --definition runtime-audit-kompiled \
  --output pretty
printf '%s\n' 'COMMAND (expected AssertionError / exit 1): krun runtime_witness_expect_true.mpy --definition runtime-audit-kompiled --output pretty'
krun runtime_witness_expect_true.mpy \
  --definition runtime-audit-kompiled \
  --output pretty
status=$?
printf 'EXIT_STATUS: %s\n' "$status"
if (( status != 1 )); then
  overall=1
fi

exit "$overall"
