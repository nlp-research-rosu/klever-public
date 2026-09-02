#!/usr/bin/env bash
set -euo pipefail
set -x

audit_project=/tmp/audit-work/lean-proof-audit
cp -a /audit-output/evidence/OperationalBridgeExpectedSemantics.lean \
  "${audit_project}/OperationalBridgeExpectedSemantics.lean"
cd "${audit_project}"
set +e
lake env lean OperationalBridgeExpectedSemantics.lean
lean_status=$?
set -e
test "${lean_status}" -ne 0
printf 'EXPECTED_NONZERO_LEAN_STATUS=%s\n' "${lean_status}"
