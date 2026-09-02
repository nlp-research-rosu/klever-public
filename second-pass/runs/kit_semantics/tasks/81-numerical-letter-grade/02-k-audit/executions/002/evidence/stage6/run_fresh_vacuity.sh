#!/usr/bin/env bash
set -u

cd /tmp/audit-work/candidate-src || exit 90

printf '$ kprove /audit-output/evidence/stage6/spec-fresh-vacuity.k --definition audit-verification-kompiled --spec-module SPEC-FRESH-VACUITY --claims SPEC-FRESH-VACUITY.correct-empty\n'
kprove /audit-output/evidence/stage6/spec-fresh-vacuity.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-FRESH-VACUITY \
  --claims SPEC-FRESH-VACUITY.correct-empty
correct_rc=$?
printf 'EXIT correct_companion=%s expected=0\n' "$correct_rc"
if (( correct_rc != 0 )); then
  exit 1
fi

printf '$ kprove /audit-output/evidence/stage6/spec-fresh-vacuity.k --definition audit-verification-kompiled --spec-module SPEC-FRESH-VACUITY --claims SPEC-FRESH-VACUITY.false-empty-return\n'
kprove /audit-output/evidence/stage6/spec-fresh-vacuity.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-FRESH-VACUITY \
  --claims SPEC-FRESH-VACUITY.false-empty-return
false_rc=$?
printf 'EXIT false_mutation=%s expected_nonzero=1\n' "$false_rc"

if (( false_rc == 0 )); then
  exit 1
fi
exit 0
