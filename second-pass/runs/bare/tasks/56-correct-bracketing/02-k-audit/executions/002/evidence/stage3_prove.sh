#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/proof || exit 90
definition=/tmp/audit-work/proof/audit-haskell-kompiled
overall=0

run_proof() {
  local description="$1"
  shift
  printf 'COMMAND (%s):' "$description"
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local proof_exit=$?
  printf 'PROOF (%s) exit=%s\n' "$description" "$proof_exit"
  if (( proof_exit != 0 )); then
    overall=1
  fi
}

run_proof "original-all-seven-claims" \
  kprove spec.k \
  --definition "$definition" \
  --spec-module SPEC

run_proof "mutually-recursive-loop-claims" \
  kprove spec-audit-labeled.k \
  --definition "$definition" \
  --spec-module SPEC-AUDIT \
  --claims SPEC-AUDIT.loop-zero,SPEC-AUDIT.loop-positive

run_proof "universal-with-loop-circularities" \
  kprove spec-audit-labeled.k \
  --definition "$definition" \
  --spec-module SPEC-AUDIT \
  --claims SPEC-AUDIT.universal-correctness,SPEC-AUDIT.loop-zero,SPEC-AUDIT.loop-positive

for label in \
  example-single-open \
  example-pair \
  example-nested \
  example-negative-prefix
do
  run_proof "$label" \
    kprove spec-audit-labeled.k \
    --definition "$definition" \
    --spec-module SPEC-AUDIT \
    --claims "SPEC-AUDIT.$label"
done

exit "$overall"
