#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work
export PATH="/usr/bin:${PATH}"

run_logged() {
  local log_name=$1
  shift
  (
    printf 'COMMAND:'
    printf ' %q' "$@"
    printf '\n'
    "$@"
    status=$?
    echo "EXIT_STATUS: ${status}"
    exit "${status}"
  ) >"/audit-output/evidence/${log_name}" 2>&1
}

run_logged 03a_runtime_kompile.log \
  kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
runtime_status=$?

run_logged 03b_concrete_krun.log \
  krun concrete_tests.mpy --definition audit-runtime-kompiled
concrete_status=$?

run_logged 03c_verification_kompile.log \
  kompile verification.k \
  --backend haskell \
  --main-module PILE-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
verification_status=$?

run_logged 03d_prefix_kprove.log \
  kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module PILE-PREFIX-SPEC
prefix_status=$?

run_logged 03e_loop_kprove.log \
  kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module PILE-LOOP-SPEC
loop_status=$?

echo "runtime_kompile=${runtime_status}"
echo "concrete_krun=${concrete_status}"
echo "verification_kompile=${verification_status}"
echo "prefix_kprove=${prefix_status}"
echo "loop_kprove=${loop_status}"

if (( runtime_status != 0 || concrete_status != 0 ||
      verification_status != 0 || prefix_status != 0 || loop_status != 0 )); then
  exit 1
fi
