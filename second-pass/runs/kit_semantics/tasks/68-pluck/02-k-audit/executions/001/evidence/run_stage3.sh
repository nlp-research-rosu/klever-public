#!/usr/bin/env bash
set -u

run_logged() {
  local label="$1"
  shift
  local log="/audit-output/evidence/${label}.log"
  {
    printf 'CWD: %s\n' "$PWD"
    printf 'COMMAND:'
    printf ' %q' "$@"
    printf '\n'
    "$@"
    local status=$?
    printf 'EXIT_STATUS: %d\n' "$status"
    return "$status"
  } >"$log" 2>&1
}

cd /tmp/audit-work/68-pluck || exit 90

if [[ -e audit-verification-kompiled ]]; then
  printf 'Refusing to reuse pre-existing audit-verification-kompiled\n' >&2
  exit 91
fi

run_logged 04-kompile-proof \
  kompile verification.k \
    --backend haskell \
    --main-module VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition audit-verification-kompiled
build_status=$?

if (( build_status != 0 )); then
  printf 'build=%d\n' "$build_status"
  exit 1
fi

run_logged 05-kprove-loop \
  kprove spec.k \
    --definition audit-verification-kompiled \
    --spec-module SPEC \
    --claims SPEC.pluck-loop
loop_status=$?

run_logged 06-kprove-entry \
  kprove spec.k \
    --definition audit-verification-kompiled \
    --spec-module SPEC \
    --claims SPEC.pluck-entry
entry_status=$?

run_logged 07-kprove-all \
  kprove spec.k \
    --definition audit-verification-kompiled \
    --spec-module SPEC
all_status=$?

printf 'build=%d loop=%d entry=%d all=%d\n' \
  "$build_status" "$loop_status" "$entry_status" "$all_status"

if (( loop_status != 0 || entry_status != 0 || all_status != 0 )); then
  exit 1
fi
