#!/usr/bin/env bash
set -uo pipefail
set -x

kompile --backend haskell \
  /tmp/audit-work/body-mutation/verification-body-mutation.k \
  --main-module VERIFICATION-BODY-MUTATION \
  --syntax-module VERIFICATION-BODY-MUTATION \
  --output-definition /tmp/audit-work/build/body-mutation-concrete-kompiled
build_status=$?

if (( build_status == 0 )); then
  krun /tmp/audit-work/body-mutation/verify-empty.mpy \
    --definition /tmp/audit-work/build/body-mutation-concrete-kompiled \
    '-cINPUT=""'
  run_status=$?
else
  run_status=125
fi

set +x
printf 'body_mutation_concrete_build_exit=%s\n' "$build_status"
printf 'body_mutation_empty_run_exit=%s\n' "$run_status"

if (( build_status != 0 || run_status != 0 )); then
  exit 1
fi
