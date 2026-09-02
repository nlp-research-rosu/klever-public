#!/usr/bin/env bash
set -u

cd /tmp/audit-work/candidate || exit 90
overall=0

printf '%s\n' 'COMMAND: kprove spec.k --definition /tmp/audit-work/proof-kompiled --spec-module SPEC --claims loop-correct'
kprove spec.k \
  --definition /tmp/audit-work/proof-kompiled \
  --spec-module SPEC \
  --claims loop-correct
status=$?
printf 'EXIT: %s\n\n' "$status"
if test "$status" -ne 0; then
  overall=1
fi

printf '%s\n' 'COMMAND: kprove spec.k --definition /tmp/audit-work/proof-kompiled --spec-module SPEC --trusted loop-correct (program-correct composition after independent loop proof)'
kprove spec.k \
  --definition /tmp/audit-work/proof-kompiled \
  --spec-module SPEC \
  --trusted loop-correct
status=$?
printf 'EXIT: %s\n\n' "$status"
if test "$status" -ne 0; then
  overall=1
fi

printf '%s\n' 'COMMAND: kprove spec.k --definition /tmp/audit-work/proof-kompiled --spec-module SPEC (all claims, including program-correct with loop-correct circularity)'
kprove spec.k \
  --definition /tmp/audit-work/proof-kompiled \
  --spec-module SPEC
status=$?
printf 'EXIT: %s\n' "$status"
if test "$status" -ne 0; then
  overall=1
fi

exit "$overall"
