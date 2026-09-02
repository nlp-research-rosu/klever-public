#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/62-derivative
cp --no-dereference \
  /audit-output/evidence/verification-no-bridge.k \
  /audit-output/evidence/spec-no-bridge.k \
  "$scratch/"
cd "$scratch" || exit 70

timeout 600 kompile verification-no-bridge.k \
  --backend haskell \
  --main-module VERIFICATION-NO-BRIDGE \
  --syntax-module VERIFICATION-NO-BRIDGE \
  --output-definition no-bridge-kompiled
build_status=$?
printf 'NO_BRIDGE_BUILD_EXIT_STATUS: %d\n' "$build_status"
if (( build_status != 0 )); then
  exit "$build_status"
fi

timeout 600 kprove spec-no-bridge.k \
  --definition no-bridge-kompiled \
  --spec-module SPEC-NO-BRIDGE \
  --claims loop-invariant-no-bridge
loop_status=$?
printf 'NO_BRIDGE_LOOP_EXIT_STATUS: %d\n' "$loop_status"
if (( loop_status != 0 )); then
  exit "$loop_status"
fi

for label in entry-empty-no-bridge entry-cons-no-bridge
do
  timeout 600 kprove spec-no-bridge.k \
    --definition no-bridge-kompiled \
    --spec-module SPEC-NO-BRIDGE \
    --claims "loop-invariant-no-bridge,$label" \
    --trusted loop-invariant-no-bridge
  status=$?
  printf 'NO_BRIDGE_%s_EXIT_STATUS: %d\n' "$label" "$status"
  if (( status != 0 )); then
    exit "$status"
  fi
done
