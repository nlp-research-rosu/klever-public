#!/usr/bin/env bash
set -u

work=/tmp/audit-work
evidence=/audit-output/evidence
cd "$work" || exit 90
cp "$evidence/audit-no-condition-bridge.k" audit-no-condition-bridge.k
cp "$evidence/spec-no-condition-bridge.k" spec-no-condition-bridge.k

run_logged() {
  local log="$1"
  shift
  echo "$ $*" | tee "$evidence/$log"
  "$@" 2>&1 | tee -a "$evidence/$log"
  local status=${PIPESTATUS[0]}
  echo "EXIT_STATUS=$status" | tee -a "$evidence/$log"
  return "$status"
}

run_logged 05a-kompile-no-condition-bridge.log \
  kompile --backend haskell audit-no-condition-bridge.k \
    --main-module AUDIT-NO-CONDITION-BRIDGE \
    --syntax-module MPY-SYNTAX \
    --output-definition audit-no-condition-bridge-kompiled
build_status=$?
if [[ "$build_status" -ne 0 ]]; then
  exit "$build_status"
fi

run_logged 05b-kprove-no-bridge-one.log \
  kprove spec-no-condition-bridge.k \
    --definition audit-no-condition-bridge-kompiled \
    --spec-module NO-CONDITION-BRIDGE-GROUND-SPEC \
    --claims NO-CONDITION-BRIDGE-GROUND-SPEC.accepted-one
one_status=$?

run_logged 05c-kprove-no-bridge-two.log \
  kprove spec-no-condition-bridge.k \
    --definition audit-no-condition-bridge-kompiled \
    --spec-module NO-CONDITION-BRIDGE-GROUND-SPEC \
    --claims NO-CONDITION-BRIDGE-GROUND-SPEC.rejected-two
two_status=$?

echo "SUMMARY build=$build_status accepted-one=$one_status rejected-two=$two_status"
if [[ "$one_status" -ne 0 || "$two_status" -ne 0 ]]; then
  exit 1
fi
exit 0
