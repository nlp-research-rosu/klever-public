#!/usr/bin/env bash
set -uo pipefail
set -x

audit_root=/tmp/audit-work/prime-length-audit
cd "$audit_root"

kompile --version
kprove --version
python3 /reference/py2mpy.py audit_concrete_tests.py > audit_concrete_tests.mpy

run_checked() {
  "$@"
  command_status=$?
  echo "EXIT_STATUS=${command_status} COMMAND=$*"
  return "$command_status"
}

overall_status=0

run_checked timeout 900s kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled || overall_status=1

if [[ "$overall_status" -eq 0 ]]; then
  run_checked timeout 300s krun audit_concrete_tests.mpy \
    --definition audit-runtime-kompiled || overall_status=1
fi

run_checked timeout 900s kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled || overall_status=1

if [[ -d audit-verification-kompiled ]]; then
  run_checked timeout 900s kprove spec.k \
    --definition audit-verification-kompiled \
    --spec-module SPEC \
    --claims SPEC.prime-length-small || overall_status=1

  run_checked timeout 900s kprove spec.k \
    --definition audit-verification-kompiled \
    --spec-module SPEC \
    --claims SPEC.prime-length-setup || overall_status=1

  run_checked timeout 900s kprove spec.k \
    --definition audit-verification-kompiled \
    --spec-module LOOP-SPEC \
    --claims LOOP-SPEC.divisor-loop || overall_status=1
fi

echo "STAGE3_OVERALL_STATUS=${overall_status}"
exit "$overall_status"
