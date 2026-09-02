#!/usr/bin/env bash
set -uo pipefail

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

scratch=/tmp/audit-work/77-iscube
src="$scratch/candidate-src"
cubedef="$scratch/audit-cube-verification-kompiled"
gapdef="$scratch/audit-gap-verification-kompiled"

printf 'Each entry proof below retains its loop claim as a circularity.\n'
printf 'A prior entry-only --claims diagnostic was interrupted because it omitted that circularity.\n'

run kprove "$src/spec.k" \
  --definition "$cubedef" \
  --spec-module CUBE-SPEC \
  --exclude CUBE-SPEC.negative-cube

run kprove "$src/spec.k" \
  --definition "$cubedef" \
  --spec-module CUBE-SPEC \
  --exclude CUBE-SPEC.nonnegative-cube

run test '!' -e "$gapdef"
run kompile "$src/verification.k" \
  --main-module GAP-VERIFICATION \
  --syntax-module GAP-VERIFICATION \
  --backend haskell \
  --output-definition "$gapdef"
gap_build_status=$?

if (( gap_build_status == 0 )); then
  run kprove "$src/spec.k" \
    --definition "$gapdef" \
    --spec-module GAP-SPEC

  run kprove "$src/spec.k" \
    --definition "$gapdef" \
    --spec-module GAP-SPEC \
    --claims GAP-SPEC.gap-loop

  run kprove "$src/spec.k" \
    --definition "$gapdef" \
    --spec-module GAP-SPEC \
    --exclude GAP-SPEC.negative-noncube

  run kprove "$src/spec.k" \
    --definition "$gapdef" \
    --spec-module GAP-SPEC \
    --exclude GAP-SPEC.positive-noncube
fi
