#!/usr/bin/env bash
set -uo pipefail

source_dir=/tmp/audit-work/94-skjkasdkd/source
definition=/tmp/audit-work/94-skjkasdkd/build/verification-kompiled
parsed_program="$source_dir/solution-parsed-expanded.kore"
macro_program="$source_dir/solution-macro-expanded.kore"

echo "COMMAND 1: kast solution.mpy --definition $definition --module MPY-SYNTAX --sort Pgm --output kore --expand-macros"
kast "$source_dir/solution.mpy" \
  --definition "$definition" \
  --module MPY-SYNTAX \
  --sort Pgm \
  --output kore \
  --expand-macros > "$parsed_program"
first_status=$?
echo "EXIT 1: $first_status"

echo "COMMAND 2: kast --expression solutionProgram --definition $definition --module VERIFICATION --sort Pgm --output kore --expand-macros"
kast \
  --expression solutionProgram \
  --definition "$definition" \
  --module VERIFICATION \
  --sort Pgm \
  --output kore \
  --expand-macros > "$macro_program"
second_status=$?
echo "EXIT 2: $second_status"

sha256sum "$parsed_program" "$macro_program"
if [[ "$first_status" -ne 0 || "$second_status" -ne 0 ]]; then
  echo "PINNING: FAIL (kast error)"
  exit 1
fi
if cmp -s "$parsed_program" "$macro_program"; then
  echo "PINNING: PASS (expanded KORE terms byte-identical)"
  exit 0
fi

echo "PINNING: FAIL (expanded KORE terms differ)"
cmp "$parsed_program" "$macro_program" || true
exit 1
