#!/usr/bin/env bash
set +e

WORK=/tmp/audit-work/57-monotonic

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

run cp /audit-output/evidence/04_verification_no_bridge.k "$WORK/verification-no-bridge.k"
run cp /audit-output/evidence/04_spec_no_bridge.k "$WORK/spec-no-bridge.k"
run cp /audit-output/evidence/04_bridge_connection_spec.k "$WORK/bridge-connection-spec.k"
run cp /audit-output/evidence/04_ground_entry_spec.k "$WORK/ground-entry-spec.k"

run kompile "$WORK/verification-no-bridge.k" \
  --backend haskell \
  --main-module MONOTONIC-VERIFICATION-NO-BRIDGE \
  --syntax-module MPY-SYNTAX \
  --output-definition "$WORK/verification-no-bridge-kompiled"

run kprove "$WORK/spec-no-bridge.k" \
  --definition "$WORK/verification-no-bridge-kompiled" \
  --spec-module MONOTONIC-SPEC-NO-BRIDGE

run kprove "$WORK/bridge-connection-spec.k" \
  --definition "$WORK/verification-no-bridge-kompiled" \
  --spec-module BRIDGE-CONNECTION-SPEC

run kprove "$WORK/ground-entry-spec.k" \
  --definition "$WORK/verification-kompiled" \
  --spec-module GROUND-ENTRY-SPEC

run krun "$WORK/concrete-smoke.mpy" \
  --definition "$WORK/verification-kompiled"
