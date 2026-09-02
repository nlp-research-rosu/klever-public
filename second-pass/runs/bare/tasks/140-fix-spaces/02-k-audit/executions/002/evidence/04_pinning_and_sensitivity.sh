#!/usr/bin/env bash
set -uo pipefail
set -x

kompile --backend haskell \
  /tmp/audit-work/pinning/verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition /tmp/audit-work/build/pinning2-kompiled
pinning_build_status=$?

if (( pinning_build_status == 0 )); then
  python3 /audit-output/evidence/04_pinning_compare.py
  pinning_compare_status=$?
else
  pinning_compare_status=125
fi

kompile --backend haskell \
  /tmp/audit-work/body-mutation/verification-body-mutation.k \
  --main-module VERIFICATION-BODY-MUTATION \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/build/body-mutation2-kompiled
body_mutation_build_status=$?

if (( body_mutation_build_status == 0 )); then
  kprove /tmp/audit-work/body-mutation/spec.k \
    --definition /tmp/audit-work/build/body-mutation2-kompiled \
    --spec-module SPEC-BODY-MUTATION
  body_mutation_proof_status=$?
else
  body_mutation_proof_status=125
fi

set +x
printf 'pinning_build_exit=%s\n' "$pinning_build_status"
printf 'pinning_compare_exit=%s\n' "$pinning_compare_status"
printf 'body_mutation_build_exit=%s\n' "$body_mutation_build_status"
printf 'body_mutation_proof_exit=%s\n' "$body_mutation_proof_status"

if (( pinning_build_status != 0 ||
      pinning_compare_status != 0 ||
      body_mutation_build_status != 0 ||
      body_mutation_proof_status == 0 )); then
  exit 1
fi
