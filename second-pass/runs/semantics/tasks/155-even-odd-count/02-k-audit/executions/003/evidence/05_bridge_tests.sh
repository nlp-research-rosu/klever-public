#!/usr/bin/env bash
set -u

run_expected_failure() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d; expected nonzero]\n' "$status"
  test "$status" -ne 0
}

run_expected_success() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d; expected zero]\n' "$status"
  test "$status" -eq 0
}

kpath="/home/agent/.nix-profile/bin:$PATH"

run_expected_failure env PATH="$kpath" \
  kprove /audit-output/evidence/05_bridge_generalization.k \
  --definition /tmp/audit-work/fresh/verification-base-kompiled \
  --spec-module AUDIT-BRIDGE-GENERALIZATION || exit $?

run_expected_failure env PATH="$kpath" \
  kprove /audit-output/evidence/05_bridge_malformed_base.k \
  --definition /tmp/audit-work/fresh/verification-base-kompiled \
  --spec-module AUDIT-BRIDGE-MALFORMED-BASE || exit $?

run_expected_success env PATH="$kpath" \
  kprove /audit-output/evidence/05_bridge_malformed_witness.k \
  --definition /tmp/audit-work/fresh/verification-kompiled \
  --spec-module AUDIT-BRIDGE-MALFORMED-WITNESS || exit $?
