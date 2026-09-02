#!/usr/bin/env bash
set -u

SCRATCH=/tmp/audit-work/anti-shuffle-audit
EVIDENCE=/audit-output/evidence

run_logged() {
  output=$1
  shift
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@" > "$output" 2>&1
  status=$?
  printf 'EXIT: %d\n' "$status"
  printf 'OUTPUT: %s\n\n' "$output"
  return "$status"
}

printf 'COMMAND: command -v kompile\n'
command -v kompile
printf 'EXIT: %d\n\n' "$?"

run_logged "$EVIDENCE/06_kompile_version.log" kompile --version
run_logged "$EVIDENCE/06_kompile_runtime.log" \
  kompile "$SCRATCH/reference-semantics/semantics.k" \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition "$SCRATCH/runtime-kompiled"
run_logged "$EVIDENCE/06_kompile_verification.log" \
  kompile "$SCRATCH/verification.k" \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition "$SCRATCH/verification-kompiled"
