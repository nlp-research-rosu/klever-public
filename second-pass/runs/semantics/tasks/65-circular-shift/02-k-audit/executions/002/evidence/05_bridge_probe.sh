#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence
cd "$scratch" || exit 2

run_logged() {
  local label=$1
  shift
  echo "\$ $*"
  "$@" 2>&1 | tee "$evidence/$label.log"
  local status=${PIPESTATUS[0]}
  echo "EXIT_STATUS=$status" | tee -a "$evidence/$label.log"
  return "$status"
}

run_logged 05a_kompile_no_bridge \
  kompile verification-no-bridge.k \
    --backend haskell \
    --main-module AUDIT-NO-BRIDGE \
    --syntax-module MPY-SYNTAX \
    --output-definition audit-no-bridge-kompiled \
    --warnings none
build_status=$?

run_logged 05b_ground_actual \
  kprove no-bridge-spec.k \
    --definition audit-no-bridge-kompiled \
    --spec-module AUDIT-NO-BRIDGE-SPEC \
    --claims AUDIT-NO-BRIDGE-SPEC.ground-actual \
    --warnings none
actual_status=$?

run_logged 05c_universal_without_bridge \
  kprove no-bridge-spec.k \
    --definition audit-no-bridge-kompiled \
    --spec-module AUDIT-NO-BRIDGE-SPEC \
    --claims AUDIT-NO-BRIDGE-SPEC.universal-connection \
    --warnings none
universal_status=$?

run_logged 05d_ground_opaque_without_bridge \
  kprove no-bridge-spec.k \
    --definition audit-no-bridge-kompiled \
    --spec-module AUDIT-NO-BRIDGE-SPEC \
    --claims AUDIT-NO-BRIDGE-SPEC.ground-opaque \
    --warnings none
opaque_status=$?

run_logged 05e_candidate_bridge_enabled \
  kprove bridge-connection-spec.k \
    --definition audit-verification-kompiled \
    --spec-module AUDIT-BRIDGE-CONNECTION-SPEC \
    --warnings none
bridge_status=$?

echo "EXPECTED: build=0 ground_actual=0 universal_without_bridge!=0 ground_opaque_without_bridge!=0 candidate_bridge_enabled=0"
echo "OBSERVED: build=$build_status ground_actual=$actual_status universal_without_bridge=$universal_status ground_opaque_without_bridge=$opaque_status candidate_bridge_enabled=$bridge_status"

if (( build_status != 0 || actual_status != 0 || universal_status == 0 ||
      opaque_status == 0 || bridge_status != 0 )); then
  exit 1
fi
exit 0
