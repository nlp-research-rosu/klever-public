#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/62-derivative
cp --no-dereference \
  /audit-output/evidence/verification-connection.k \
  /audit-output/evidence/spec-connection.k \
  "$scratch/"
cd "$scratch" || exit 70

timeout 600 kompile verification-connection.k \
  --backend haskell \
  --main-module VERIFICATION-CONNECTION \
  --syntax-module VERIFICATION-CONNECTION \
  --output-definition connection-kompiled
build_status=$?
printf 'CONNECTION_BUILD_EXIT_STATUS: %d\n' "$build_status"
if (( build_status != 0 )); then
  exit "$build_status"
fi

timeout 600 kprove spec-connection.k \
  --definition connection-kompiled \
  --spec-module SPEC-CONNECTION \
  --claims eager-enum-characterization
prove_status=$?
printf 'CONNECTION_PROVE_EXIT_STATUS: %d\n' "$prove_status"
exit "$prove_status"
