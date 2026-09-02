#!/usr/bin/env bash
set +e

WORK=/tmp/audit-work/source
EVIDENCE=/audit-output/evidence
overall=0

run_kast() {
  local source=$1
  local output=$2
  printf 'COMMAND: kast %s --definition %s --module GCD-VERIFICATION --sort Module --expand-macros --output kore --output-file %s\n' \
    "$source" "$WORK/verification-kompiled" "$output"
  kast "$source" \
    --definition "$WORK/verification-kompiled" \
    --module GCD-VERIFICATION \
    --sort Module \
    --expand-macros \
    --output kore \
    --output-file "$output"
  local status=$?
  printf 'EXIT STATUS: %d\n' "$status"
  if (( status != 0 )); then
    overall=1
  fi
}

run_kast "$WORK/solution.regenerated.mpy" "$WORK/solution.expanded.kore"
run_kast "$EVIDENCE/macro_program.mpy" "$WORK/macro_program.expanded.kore"

printf 'COMMAND: cmp -s %s %s\n' \
  "$WORK/solution.expanded.kore" "$WORK/macro_program.expanded.kore"
cmp -s "$WORK/solution.expanded.kore" "$WORK/macro_program.expanded.kore"
status=$?
printf 'EXPANDED KORE IDENTITY EXIT STATUS: %d\n' "$status"
if (( status != 0 )); then
  overall=1
  diff -u "$WORK/solution.expanded.kore" "$WORK/macro_program.expanded.kore"
fi

printf 'COMMAND: sha256sum %s %s\n' \
  "$WORK/solution.expanded.kore" "$WORK/macro_program.expanded.kore"
sha256sum "$WORK/solution.expanded.kore" "$WORK/macro_program.expanded.kore"
status=$?
printf 'SHA256 EXIT STATUS: %d\n' "$status"
if (( status != 0 )); then
  overall=1
fi

printf 'STAGE 4 PINNING EXIT STATUS: %d\n' "$overall"
exit "$overall"
