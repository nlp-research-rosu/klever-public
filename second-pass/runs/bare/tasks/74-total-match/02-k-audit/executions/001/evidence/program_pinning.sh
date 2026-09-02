#!/usr/bin/env bash
set -uo pipefail

definition=/tmp/audit-work/build/verification-kompiled
actual=/tmp/audit-work/program-actual-expanded.json
macro=/tmp/audit-work/program-macro-expanded.json

kast /tmp/audit-work/src/solution.mpy \
  --definition "$definition" \
  --module VERIFICATION \
  --sort Program \
  --output json \
  --expand-macros \
  > "$actual"
actual_status=$?

kast --expression solutionProgram \
  --definition "$definition" \
  --module VERIFICATION \
  --sort Program \
  --output json \
  --expand-macros \
  > "$macro"
macro_status=$?

echo "ACTUAL_KAST_EXIT: $actual_status"
echo "MACRO_KAST_EXIT: $macro_status"
if (( actual_status != 0 || macro_status != 0 )); then
  exit 1
fi

sha256sum "$actual" "$macro"
if ! cmp -s "$actual" "$macro"; then
  echo "EXPANDED_KAST_IDENTITY: FAIL"
  diff -u "$actual" "$macro"
  exit 1
fi

echo "EXPANDED_KAST_IDENTITY: PASS"
cp "$actual" /audit-output/evidence/program-actual-expanded.json
cp "$macro" /audit-output/evidence/program-macro-expanded.json
