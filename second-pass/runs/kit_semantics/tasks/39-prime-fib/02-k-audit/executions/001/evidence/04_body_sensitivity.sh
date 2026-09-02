#!/usr/bin/env bash
set -u
set -o pipefail

scratch=/tmp/audit-work/39-prime-fib-audit
log=/audit-output/evidence/04_body_sensitivity.log
cp /audit-output/evidence/04_body_sensitivity.k "$scratch/body-sensitivity.k"

cd "$scratch"
set +e
(
  printf '%s\n' '$ kprove body-sensitivity.k --definition verification-audit-kompiled --spec-module AUDIT-BODY-SENSITIVITY --claims SPEC.inner-loop,SPEC.outer-loop,AUDIT-BODY-SENSITIVITY.changed-initial-b-to-3 --trusted SPEC.inner-loop,SPEC.outer-loop'
  kprove body-sensitivity.k \
    --definition verification-audit-kompiled \
    --spec-module AUDIT-BODY-SENSITIVITY \
    --claims SPEC.inner-loop,SPEC.outer-loop,AUDIT-BODY-SENSITIVITY.changed-initial-b-to-3 \
    --trusted SPEC.inner-loop,SPEC.outer-loop
  rc=$?
  printf '[exit %d]\n' "$rc"
  exit "$rc"
) > "$log" 2>&1
rc=$?
set -e

if [[ "$rc" -eq 0 ]]; then
  echo "ERROR: changed executed body unexpectedly proved the old destination"
  exit 1
fi
if ! grep -q 'WarnStuckClaimState' "$log"; then
  echo "ERROR: changed-body probe did not reach an unmet proof obligation"
  exit 1
fi
if ! grep -q '<k>' "$log" || ! grep -q '^      3 ~> .K' "$log"; then
  echo "ERROR: residual did not expose the changed body's concrete result 3"
  exit 1
fi
if ! grep -q 'Assign ( Name ( \"b\" ) , Int ( 3 ) )' "$log"; then
  echo "ERROR: residual did not retain the changed executed closure"
  exit 1
fi
echo "EXPECTED BODY-SENSITIVITY FAILURE: executed body changed b=1 to b=3; residual result is 3"
