#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction

run() {
  printf '+'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS=%d\n' "$status"
  return "$status"
}

run kompile --version || exit $?
run krun --version || exit $?
run kprove --version || exit $?
run test ! -e "$work/semantic-kompiled" || exit $?
run test ! -e "$work/proof-kompiled" || exit $?

run kompile "$work/semantic.k" \
  --backend llvm \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition "$work/semantic-kompiled" || exit $?

run python3 /audit-output/evidence/03-concrete-compare.py || exit $?

run kompile "$work/verification.k" \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$work/proof-kompiled" || exit $?

run kprove "$work/spec.k" \
  --definition "$work/proof-kompiled" \
  --spec-module SPEC || exit $?

claims=(
  universal
  example-1
  example-2
  example-3
  example-4
  example-5
  example-6
)

for claim in "${claims[@]}"; do
  run kprove "$work/spec-labeled.k" \
    --definition "$work/proof-kompiled" \
    --spec-module SPEC-LABELED \
    --claims "SPEC-LABELED.$claim" || exit $?
done
