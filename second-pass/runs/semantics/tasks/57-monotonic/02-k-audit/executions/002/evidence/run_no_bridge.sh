#!/usr/bin/env bash
set -euo pipefail

scratch=/tmp/audit-work/candidate
build_root=/tmp/audit-work/no-bridge-build
mkdir -p "$build_root"
cp /audit-output/evidence/verification-no-bridge.k "$scratch/verification-no-bridge.k"
cp /audit-output/evidence/spec-no-bridge.k "$scratch/spec-no-bridge.k"

printf 'COMMAND: kompile %s --backend haskell --main-module MONOTONIC-VERIFICATION-NO-BRIDGE --syntax-module MPY-SYNTAX --output-definition %s\n' \
  "$scratch/verification-no-bridge.k" "$build_root/verification-kompiled"
kompile "$scratch/verification-no-bridge.k" \
  --backend haskell \
  --main-module MONOTONIC-VERIFICATION-NO-BRIDGE \
  --syntax-module MPY-SYNTAX \
  --output-definition "$build_root/verification-kompiled"
printf 'EXIT_STATUS=0\n'

printf 'COMMAND: kprove %s --definition %s --spec-module MONOTONIC-SPEC-NO-BRIDGE\n' \
  "$scratch/spec-no-bridge.k" "$build_root/verification-kompiled"
set +e
kprove "$scratch/spec-no-bridge.k" \
  --definition "$build_root/verification-kompiled" \
  --spec-module MONOTONIC-SPEC-NO-BRIDGE \
  >"$build_root/kprove.raw.log" 2>&1
status=$?
set -e
sed -n '1,100p' "$build_root/kprove.raw.log"
rg -n -m 80 'WarnStuckClaimState|==K|sortVS|\\[Error\\]' "$build_root/kprove.raw.log" || true
tail -25 "$build_root/kprove.raw.log"
printf 'EXIT_STATUS=%s\n' "$status"
if [ "$status" -eq 0 ]; then
  printf 'EXPECTED_NONZERO_BUT_SUCCEEDED\n'
  exit 1
fi
if ! rg -q 'WarnStuckClaimState' "$build_root/kprove.raw.log"; then
  printf 'EXPECTED_STUCK_CLAIM_NOT_FOUND\n'
  exit 1
fi
printf 'NO_BRIDGE_DEPENDENCY_PROBE=PASS\n'
