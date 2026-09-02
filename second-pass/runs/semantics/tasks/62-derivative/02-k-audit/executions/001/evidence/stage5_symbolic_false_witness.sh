#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/62-derivative
cp --no-dereference \
  /audit-output/evidence/spec-bridge-symbolic-false.k \
  "$scratch/"
cd "$scratch" || exit 70

timeout 300 kprove spec-bridge-symbolic-false.k \
  --definition verification-kompiled \
  --spec-module SPEC-BRIDGE-SYMBOLIC-FALSE \
  --claims symbolic-enum-always-nonempty
status=$?
printf 'SYMBOLIC_FALSE_WITNESS_EXIT_STATUS: %d\n' "$status"
exit "$status"
