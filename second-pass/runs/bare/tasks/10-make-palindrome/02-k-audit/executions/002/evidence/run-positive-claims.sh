#!/usr/bin/env bash
set -euo pipefail

work=/tmp/audit-work/candidate
logger=/audit-output/evidence/run-logged.sh

cd "$work"

"$logger" /audit-output/evidence/stage3-kprove-SPEC-functional-correctness-repeat.log \
  kprove spec.k \
  --definition "$work/fresh-semantic-proof-kompiled" \
  --spec-module SPEC \
  --claims SPEC.functional-correctness \
  -w none

"$logger" /audit-output/evidence/stage3-kprove-SPEC-helper-correctness.log \
  kprove spec.k \
  --definition "$work/fresh-semantic-proof-kompiled" \
  --spec-module SPEC \
  --claims SPEC.helper-correctness \
  -w none

for label in empty cat cata xyx abcd aabb; do
  "$logger" "/audit-output/evidence/stage3-kprove-CONCRETE-SPEC-${label}.log" \
    kprove spec.k \
    --definition "$work/fresh-execution-proof-kompiled" \
    --spec-module CONCRETE-SPEC \
    --claims "CONCRETE-SPEC.${label}" \
    -w none
done
