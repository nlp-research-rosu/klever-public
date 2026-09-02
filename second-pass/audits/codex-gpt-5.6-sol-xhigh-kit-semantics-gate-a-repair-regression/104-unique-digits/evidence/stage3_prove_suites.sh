#!/usr/bin/env bash
set -uo pipefail

runner=/audit-output/evidence/run_logged.sh
work=/tmp/audit-work/104-unique-digits-audit/candidate-source
overall_status=0

cd "$work" || exit 1

"$runner" /audit-output/evidence/stage3_connection_suite.log \
  kprove connection-spec.k \
    --definition /tmp/audit-work/104-unique-digits-audit/connection-fresh-kompiled \
    --spec-module CONNECTION-SPEC
connection_status=$?
(( connection_status == 0 )) || overall_status=1

"$runner" /audit-output/evidence/stage3_target_suite.log \
  kprove spec.k \
    --definition /tmp/audit-work/104-unique-digits-audit/verification-fresh-kompiled \
    --spec-module SPEC
target_status=$?
(( target_status == 0 )) || overall_status=1

"$runner" /audit-output/evidence/stage3_ground_bridge_suite.log \
  kprove audit-spec.k \
    --definition /tmp/audit-work/104-unique-digits-audit/audit-fresh-kompiled \
    --spec-module AUDIT-SPEC
ground_status=$?
(( ground_status == 0 )) || overall_status=1

printf 'CONNECTION_SUITE_STATUS: %d\n' "$connection_status"
printf 'TARGET_SUITE_STATUS: %d\n' "$target_status"
printf 'GROUND_BRIDGE_SUITE_STATUS: %d\n' "$ground_status"
printf 'ALL_SUITES_STATUS: %d\n' "$overall_status"
exit "$overall_status"
