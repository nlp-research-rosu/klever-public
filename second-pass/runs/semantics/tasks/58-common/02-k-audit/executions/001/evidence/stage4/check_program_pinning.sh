#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/case58
evidence=/audit-output/evidence/stage4

kast --definition "$scratch/verification-kompiled" \
  --module VERIFICATION --input program --output kore \
  "$scratch/solution.mpy" > "$evidence/submitted-program.kore"
submitted_status=$?
printf 'submitted-kast-exit=%d\n' "$submitted_status"

kast --definition "$scratch/verification-kompiled" \
  --module VERIFICATION --input program --output kore \
  "$evidence/macro-program.mpy" > "$evidence/macro-program.kore"
macro_status=$?
printf 'macro-kast-exit=%d\n' "$macro_status"

if (( submitted_status != 0 || macro_status != 0 )); then
  exit 1
fi

sha256sum "$evidence/submitted-program.kore" "$evidence/macro-program.kore"
if cmp -s "$evidence/submitted-program.kore" "$evidence/macro-program.kore"; then
  printf 'IDENTICAL_KORE submitted solution.mpy == Module(commonDefinition)\n'
  exit 0
fi

printf 'DIFFERENT_KORE submitted solution.mpy != Module(commonDefinition)\n'
diff -u "$evidence/submitted-program.kore" "$evidence/macro-program.kore" || true
exit 1
