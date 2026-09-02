#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/132-is-nested-review || exit 90
cp /audit-output/evidence/auditor-false-spec.k auditor-false-spec.k

echo '$ kprove auditor-false-spec.k --definition verification-kompiled-fresh --spec-module AUDITOR-FALSE-SPEC --dry-run'
kprove auditor-false-spec.k \
  --definition verification-kompiled-fresh \
  --spec-module AUDITOR-FALSE-SPEC \
  --dry-run
dry_status=$?
echo "EXIT_STATUS: ${dry_status}"
if [ "${dry_status}" -ne 0 ]; then
  echo "ERROR: mutation did not parse/build"
  exit 20
fi

echo '$ kprove auditor-false-spec.k --definition verification-kompiled-fresh --spec-module AUDITOR-FALSE-SPEC'
set +e
kprove auditor-false-spec.k \
  --definition verification-kompiled-fresh \
  --spec-module AUDITOR-FALSE-SPEC \
  2>&1 | tee /audit-output/evidence/stage6_false_proof_raw.log
proof_status=${PIPESTATUS[0]}
set -e
echo "EXIT_STATUS: ${proof_status}"
if [ "${proof_status}" -eq 0 ]; then
  echo "ERROR: demonstrably false mutation unexpectedly proved"
  exit 21
fi

echo '$ rg -n "WarnStuckClaimState|false|true|implication check" /audit-output/evidence/stage6_false_proof_raw.log'
rg -n 'WarnStuckClaimState|false|true|implication check' \
  /audit-output/evidence/stage6_false_proof_raw.log
residual_status=$?
echo "EXIT_STATUS: ${residual_status}"
if [ "${residual_status}" -ne 0 ]; then
  echo "ERROR: nonzero proof lacked the expected unmet-result residual"
  exit 22
fi

echo "EXPECTED_FAILURE_CONFIRMED: build=0 proof=${proof_status} satisfying_input=empty actual=false mutated_target=true"
