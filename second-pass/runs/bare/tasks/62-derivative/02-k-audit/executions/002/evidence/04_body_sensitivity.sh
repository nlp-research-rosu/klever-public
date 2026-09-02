#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/reconstruction-62 || exit 70

build=(
  kompile verification-body-mutation.k
  --main-module VERIFICATION-BODY-MUTATION
  --syntax-module VERIFICATION-BODY-MUTATION
  --backend haskell
  -o verification-body-mutation-kompiled
)
printf 'COMMAND:'
printf ' %q' "${build[@]}"
printf '\n'
"${build[@]}"
build_status=$?
printf 'EXIT_STATUS: %d\n' "$build_status"
if (( build_status != 0 )); then
  exit "$build_status"
fi

prove=(
  timeout 120s
  kprove spec-body-mutation.k
  --definition verification-body-mutation-kompiled
  --spec-module SPEC-BODY-MUTATION
)
printf 'COMMAND:'
printf ' %q' "${prove[@]}"
printf '\n'
"${prove[@]}"
prove_status=$?
printf 'EXIT_STATUS: %d\n' "$prove_status"

if (( prove_status == 0 )); then
  echo "UNEXPECTED: body mutation proved"
  exit 1
fi
if (( prove_status == 124 )); then
  echo "UNEXPECTED: body mutation timed out"
  exit 2
fi
echo "EXPECTED_FAILURE: constructor-level body mutation invalidated the helper theorem"
exit 0
