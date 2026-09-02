#!/usr/bin/env bash
set -uo pipefail
cd /tmp/audit-work

echo 'COMMAND: fresh false result mutation'
echo 'kprove reviewer-spec-vacuity.k --definition replay-verification-kompiled --spec-module REVIEWER-SPEC-VACUITY'
kprove reviewer-spec-vacuity.k \
  --definition replay-verification-kompiled \
  --spec-module REVIEWER-SPEC-VACUITY \
  > /tmp/audit-work/reviewer-vacuity.actual 2>&1
vacuity_status=$?
cat /tmp/audit-work/reviewer-vacuity.actual
echo "EXIT: $vacuity_status"

echo 'COMMAND: fresh body-sensitivity mutation'
echo 'kprove reviewer-spec-body-mutation.k --definition replay-verification-kompiled --spec-module REVIEWER-SPEC-BODY-MUTATION'
kprove reviewer-spec-body-mutation.k \
  --definition replay-verification-kompiled \
  --spec-module REVIEWER-SPEC-BODY-MUTATION \
  > /tmp/audit-work/reviewer-body.actual 2>&1
body_status=$?
cat /tmp/audit-work/reviewer-body.actual
echo "EXIT: $body_status"

if [[ "$vacuity_status" -eq 1 ]] \
  && rg -q 'WarnStuckClaimState' /tmp/audit-work/reviewer-vacuity.actual \
  && rg -q '<k>[[:space:]]*$' /tmp/audit-work/reviewer-vacuity.actual \
  && rg -q 'WarnStuckClaimState' /tmp/audit-work/reviewer-body.actual \
  && [[ "$body_status" -eq 1 ]]
then
  echo 'EXPECTED_FAILURES_CONFIRMED=1'
  exit 0
fi

echo 'EXPECTED_FAILURES_CONFIRMED=0'
exit 1
