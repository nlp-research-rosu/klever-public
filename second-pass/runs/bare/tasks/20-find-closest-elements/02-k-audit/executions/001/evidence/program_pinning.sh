#!/usr/bin/env bash
set -uo pipefail

definition=/tmp/audit-work/build/verification-llvm-kompiled
submitted=/tmp/audit-work/source/solution.mpy
symbol=/audit-output/evidence/solution-symbol.run
output_directory=/tmp/audit-work/pinning
mkdir -p "$output_directory"

printf 'COMMAND: krun %q --definition %q --output kore > %q\n' \
  "$submitted" "$definition" "$output_directory/submitted.kore"
krun "$submitted" --definition "$definition" --output kore \
  >"$output_directory/submitted.kore" \
  2>"$output_directory/submitted.stderr"
submitted_status=$?
printf 'SUBMITTED_EXIT_STATUS: %d\n' "$submitted_status"

printf 'COMMAND: krun %q --definition %q --output kore > %q\n' \
  "$symbol" "$definition" "$output_directory/symbol.kore"
krun "$symbol" --definition "$definition" --output kore \
  >"$output_directory/symbol.kore" \
  2>"$output_directory/symbol.stderr"
symbol_status=$?
printf 'SYMBOL_EXIT_STATUS: %d\n' "$symbol_status"

printf 'COMMAND: cmp -- %q %q\n' \
  "$output_directory/submitted.kore" "$output_directory/symbol.kore"
cmp -- "$output_directory/submitted.kore" "$output_directory/symbol.kore"
compare_status=$?
printf 'KORE_OUTPUT_CMP_STATUS: %d\n' "$compare_status"
sha256sum "$output_directory/submitted.kore" "$output_directory/symbol.kore"

printf 'SUBMITTED_STDERR:\n'
sed -n '1,80p' "$output_directory/submitted.stderr"
printf 'SYMBOL_STDERR:\n'
sed -n '1,80p' "$output_directory/symbol.stderr"

if (( submitted_status != 0 )); then
  exit "$submitted_status"
fi
if (( symbol_status != 0 )); then
  exit "$symbol_status"
fi
exit "$compare_status"
