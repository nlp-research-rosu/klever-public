#!/usr/bin/env bash
set +e

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

scratch=/tmp/audit-work/102-choose-num
definition="$scratch/verification-kompiled"
spec="$scratch/spec.k"

printf 'Stage 3 clean proof reconstruction and per-claim runs\n'
run kprove --version
run test ! -e "$definition"

run kompile "$scratch/verification.k" \
  --backend haskell \
  --main-module CHOOSE-NUM-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$definition"

for label in \
  all-positive-inputs \
  even-upper-in-range \
  even-upper-before-range \
  odd-upper-predecessor-in-range \
  odd-upper-no-even-in-range
do
  run kprove "$spec" \
    --definition "$definition" \
    --spec-module CHOOSE-NUM-SPEC \
    --claims "CHOOSE-NUM-SPEC.$label"
done
