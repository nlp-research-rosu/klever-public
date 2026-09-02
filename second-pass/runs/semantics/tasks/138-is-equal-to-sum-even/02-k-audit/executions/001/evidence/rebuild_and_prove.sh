#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/review-138
evidence=/audit-output/evidence
cd "$work" || exit 99

run_logged() {
  local log="$1"
  shift
  {
    printf 'WORKDIR: %s\n' "$PWD"
    printf 'COMMAND:'
    printf ' %q' "$@"
    printf '\n'
    "$@"
    status=$?
    printf 'EXIT_STATUS: %s\n' "$status"
    exit "$status"
  } 2>&1 | tee "$evidence/$log"
  return "${PIPESTATUS[0]}"
}

run_logged toolchain.log kompile --version
run_logged build-verification.log \
  kompile verification.k \
    --backend haskell \
    --main-module VERIFICATION \
    --syntax-module VERIFICATION \
    --output-definition verification-kompiled
build_status=$?

if [[ "$build_status" -ne 0 ]]; then
  exit "$build_status"
fi

overall=0
run_logged prove-all.log \
  kprove spec.k \
    --definition verification-kompiled \
    --spec-module SPEC || overall=1
run_logged prove-main.log \
  kprove spec-main.k \
    --definition verification-kompiled \
    --spec-module SPEC-MAIN || overall=1
run_logged prove-true.log \
  kprove spec-true.k \
    --definition verification-kompiled \
    --spec-module SPEC-TRUE || overall=1
run_logged prove-low.log \
  kprove spec-low.k \
    --definition verification-kompiled \
    --spec-module SPEC-LOW || overall=1
run_logged prove-nonzero.log \
  kprove spec-nonzero.k \
    --definition verification-kompiled \
    --spec-module SPEC-NONZERO || overall=1

exit "$overall"
