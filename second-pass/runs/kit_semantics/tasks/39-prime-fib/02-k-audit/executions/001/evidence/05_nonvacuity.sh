#!/usr/bin/env bash
set -u
set -o pipefail

scratch=/tmp/audit-work/39-prime-fib-audit
log=/audit-output/evidence/05_false_n5.log
cp /audit-output/evidence/05_false_n5.k "$scratch/false-n5.k"

cd "$scratch"
set +e
(
  printf '%s\n' '$ kprove false-n5.k --definition verification-audit-kompiled --spec-module AUDIT-FALSE-N5 --claims SPEC.inner-loop,SPEC.outer-loop,AUDIT-FALSE-N5.false-n5-result --trusted SPEC.inner-loop,SPEC.outer-loop'
  kprove false-n5.k \
    --definition verification-audit-kompiled \
    --spec-module AUDIT-FALSE-N5 \
    --claims SPEC.inner-loop,SPEC.outer-loop,AUDIT-FALSE-N5.false-n5-result \
    --trusted SPEC.inner-loop,SPEC.outer-loop
  rc=$?
  printf '[exit %d]\n' "$rc"
  exit "$rc"
) > "$log" 2>&1
rc=$?
set -e

if [[ "$rc" -eq 0 ]]; then
  echo "ERROR: false N=5 result unexpectedly proved"
  exit 1
fi
if ! grep -q 'WarnStuckClaimState' "$log"; then
  echo "ERROR: mutation failed without the expected unmet proof obligation"
  exit 1
fi
if ! grep -q '88' "$log"; then
  echo "ERROR: residual does not retain the false destination 88"
  exit 1
fi
printf 'EXPECTED PROOF FAILURE: exit=%d, WarnStuckClaimState present, false destination 88 present\n' "$rc"
