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

run_logged build-fixed-semantics.log \
  kompile reference-semantics/semantics.k \
    --backend haskell \
    --main-module MPY \
    --syntax-module MPY-SYNTAX \
    --output-definition fixed-semantics-kompiled
build_status=$?
if [[ "$build_status" -ne 0 ]]; then
  exit "$build_status"
fi

run_logged prove-fixed-real-program.log \
  kprove spec-fixed-real-program.k \
    --definition fixed-semantics-kompiled \
    --spec-module SPEC-FIXED-REAL-PROGRAM
