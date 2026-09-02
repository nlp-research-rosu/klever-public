#!/usr/bin/env bash
set -uo pipefail

WORK=/tmp/audit-work/reconstruction

record_status() {
  local label="$1"
  local status="$2"
  printf 'STATUS [%s]: %s\n' "$label" "$status"
  if [[ "$status" -ne 0 ]]; then
    exit "$status"
  fi
}

cd "$WORK" || exit 1

printf '%s\n' \
  'COMMAND: kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition fresh-verification-kompiled'
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-verification-kompiled
status=$?
record_status "fresh Haskell kompile" "$status"

printf '%s\n' \
  'COMMAND: kprove spec.k --definition fresh-verification-kompiled --spec-module SPEC'
kprove spec.k \
  --definition fresh-verification-kompiled \
  --spec-module SPEC
status=$?
record_status "positive target claim SPEC.generate-integers" "$status"

printf '%s\n' 'RESULT: every positive target claim closed'
