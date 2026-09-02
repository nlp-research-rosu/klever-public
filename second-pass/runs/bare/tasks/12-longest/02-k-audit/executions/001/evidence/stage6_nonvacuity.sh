#!/usr/bin/env bash
set -euo pipefail
cd /tmp/audit-work/12-longest-audit

export PATH="/home/agent/.nix-profile/bin:$PATH"
cp /audit-output/evidence/spec-vacuity.k spec-vacuity.k

echo '$ build/parse mutation with kprove --dry-run'
set +e
dry_output="$(
  kprove spec-vacuity.k \
    --definition verification-fresh-kompiled \
    --spec-module SPEC-VACUITY \
    --dry-run \
    --output pretty \
    2>&1
)"
dry_status=$?
set -e
printf '%s\n' "$dry_output"
echo "DRY_RUN_EXIT_STATUS=$dry_status"
if [[ $dry_status -ne 0 ]]; then
  echo 'ERROR: mutation did not build'
  exit 1
fi

echo '$ prove deliberately false result mutation'
set +e
proof_output="$(
  kprove spec-vacuity.k \
    --definition verification-fresh-kompiled \
    --spec-module SPEC-VACUITY \
    --output pretty \
    2>&1
)"
proof_status=$?
set -e

# Retain the full output in scratch and bounded diagnostic excerpts here.
printf '%s\n' "$proof_output" > mutation-full-output.log
echo "KPROVE_EXIT_STATUS=$proof_status"
echo '--- first 100 lines ---'
printf '%s\n' "$proof_output" | sed -n '1,100p'
echo '--- last 100 lines ---'
printf '%s\n' "$proof_output" | tail -n 100

if [[ $proof_status -eq 0 ]]; then
  echo 'ERROR: false mutation unexpectedly closed'
  exit 1
fi
if ! printf '%s\n' "$proof_output" | rg -q 'WarnStuckClaimState'; then
  echo 'ERROR: failure was not an expected stuck reachability obligation'
  exit 1
fi
if ! printf '%s\n' "$proof_output" | rg -q 'strVal.*"ccc"|\\x63\\x63\\x63'; then
  echo 'ERROR: residual did not expose the actual ccc result'
  exit 1
fi

echo 'EXPECTED_FALSE_MUTATION_REJECTED=PASS'
echo 'SCRIPT_EXIT_STATUS=0'
