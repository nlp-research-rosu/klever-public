#!/usr/bin/env bash
set -uo pipefail

SCRATCH=/tmp/audit-work/59-lpf
EVIDENCE=/audit-output/evidence

run_logged() {
  log=$1
  shift
  {
    echo "\$ $*"
    "$@"
    status=$?
    echo "[exit $status]"
    exit "$status"
  } 2>&1 | tee "$EVIDENCE/$log"
  return "${PIPESTATUS[0]}"
}

cd "$SCRATCH" || exit 1

run_logged 04_versions.log kompile --version || exit $?
run_logged 04_runtime_kompile.log \
  kompile reference-semantics/semantics.k \
    --backend llvm \
    --main-module MPY-KRUN \
    --syntax-module MPY-SYNTAX \
    --output-definition audit-runtime-kompiled || exit $?

run_logged 04_concrete_krun.log \
  krun concrete-tests.mpy \
    --definition audit-runtime-kompiled || exit $?

run_logged 04_verification_kompile.log \
  kompile verification.k \
    --backend haskell \
    --main-module VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition audit-verification-kompiled || exit $?

run_logged 04_kprove_lpf_loop.log \
  kprove spec.k \
    --definition audit-verification-kompiled \
    --spec-module SPEC \
    --claims SPEC.lpf-loop || exit $?

run_logged 04_kprove_entry.log \
  kprove spec.k \
    --definition audit-verification-kompiled \
    --spec-module SPEC \
    --claims SPEC.largest-prime-factor-entry || exit $?

run_logged 04_kprove_all.log \
  kprove spec.k \
    --definition audit-verification-kompiled \
    --spec-module SPEC || exit $?
