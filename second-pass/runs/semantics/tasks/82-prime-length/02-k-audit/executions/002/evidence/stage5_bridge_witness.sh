#!/usr/bin/env bash
set -uo pipefail
set -x

cd /tmp/audit-work/prime-length-audit

run_record() {
  expected_status=$1
  shift
  "$@"
  command_status=$?
  echo "EXIT_STATUS=${command_status} EXPECTED=${expected_status} COMMAND=$*"
  if [[ "$expected_status" == "zero" && "$command_status" -ne 0 ]]; then
    return 1
  fi
  if [[ "$expected_status" == "nonzero" && "$command_status" -eq 0 ]]; then
    return 1
  fi
  return 0
}

overall_status=0
run_record zero timeout 900s kompile verification-fixed.k \
  --backend haskell \
  --main-module VERIFICATION-FIXED \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-fixed-kompiled || overall_status=1

run_record zero timeout 900s kprove bridge-witness-extended.k \
  --definition audit-verification-kompiled \
  --spec-module BRIDGE-WITNESS-EXTENDED \
  --claims BRIDGE-WITNESS-EXTENDED.fabricated-marker || overall_status=1

run_record zero timeout 900s kprove bridge-witness-fixed.k \
  --definition audit-fixed-kompiled \
  --spec-module BRIDGE-WITNESS-FIXED \
  --claims BRIDGE-WITNESS-FIXED.real-result || overall_status=1

run_record nonzero timeout 900s kprove bridge-witness-fixed.k \
  --definition audit-fixed-kompiled \
  --spec-module BRIDGE-WITNESS-FIXED \
  --claims BRIDGE-WITNESS-FIXED.fabricated-marker || overall_status=1

echo "STAGE5_BRIDGE_WITNESS_STATUS=${overall_status}"
exit "$overall_status"
