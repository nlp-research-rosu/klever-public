#!/usr/bin/env bash
set -u

FRESH=/tmp/audit-work/fresh
overall=0

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  if (( status != 0 )); then
    overall=1
  fi
}

run find "$FRESH" -maxdepth 2 -printf '%y|%p|%s|%l\n'

run kompile "$FRESH/semantic.k" \
  --backend llvm \
  --main-module MODP-SEMANTIC \
  --syntax-module MODP-SYNTAX \
  --output-definition "$FRESH/concrete-kompiled"

if [[ -d "$FRESH/concrete-kompiled" ]]; then
  run python3 /audit-output/evidence/03_concrete_compare.py
else
  printf '\n[SKIP] concrete comparison: concrete-kompiled was not created\n'
  overall=1
fi

run kompile "$FRESH/verification.k" \
  --backend haskell \
  --main-module MODP-VERIFICATION \
  --syntax-module MODP-SYNTAX \
  --output-definition "$FRESH/proof-kompiled"

if [[ -d "$FRESH/proof-kompiled" ]]; then
  run kprove "$FRESH/spec.k" \
    --definition "$FRESH/proof-kompiled" \
    --spec-module MODP-SPEC

  run kprove "$FRESH/audit-positive-general.k" \
    --definition "$FRESH/proof-kompiled" \
    --spec-module AUDIT-POSITIVE-GENERAL

  run kprove "$FRESH/audit-positive-example-1.k" \
    --definition "$FRESH/proof-kompiled" \
    --spec-module AUDIT-POSITIVE-EXAMPLE-1

  run kprove "$FRESH/audit-positive-example-2.k" \
    --definition "$FRESH/proof-kompiled" \
    --spec-module AUDIT-POSITIVE-EXAMPLE-2

  run kprove "$FRESH/audit-positive-example-3.k" \
    --definition "$FRESH/proof-kompiled" \
    --spec-module AUDIT-POSITIVE-EXAMPLE-3

  run kprove "$FRESH/audit-positive-example-4.k" \
    --definition "$FRESH/proof-kompiled" \
    --spec-module AUDIT-POSITIVE-EXAMPLE-4

  run kprove "$FRESH/audit-positive-example-5.k" \
    --definition "$FRESH/proof-kompiled" \
    --spec-module AUDIT-POSITIVE-EXAMPLE-5
else
  printf '\n[SKIP] positive proofs: proof-kompiled was not created\n'
  overall=1
fi

printf '\nOVERALL_EXIT=%d\n' "$overall"
exit "$overall"
