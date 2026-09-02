#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/reconstruction-62 || exit 70

printf '%s\n' \
  "COMMAND: python3 -c 'from solution import derivative; print(derivative([0, True, False, True])); print(derivative([0.0, 1.5, -2.0]))'"
python3 -c 'from solution import derivative; print(derivative([0, True, False, True])); print(derivative([0.0, 1.5, -2.0]))'
printf 'EXIT_STATUS: %d\n' "$?"

k_command=(
  krun solution.mpy
  --definition semantic-fresh-kompiled
  '-cARGS=ListV(IntV(0), BoolV(true), BoolV(false), BoolV(true))'
)
printf 'COMMAND:'
printf ' %q' "${k_command[@]}"
printf '\n'
"${k_command[@]}"
printf 'EXIT_STATUS: %d\n' "$?"

float_parse=(
  kast
  --expression 'ListV(FloatV(0.0), FloatV(1.5), FloatV(-2.0))'
  --definition semantic-fresh-kompiled
  --module MPY
  --sort Value
)
printf 'COMMAND:'
printf ' %q' "${float_parse[@]}"
printf '\n'
"${float_parse[@]}"
float_status=$?
printf 'EXIT_STATUS: %d\n' "$float_status"
if (( float_status == 0 )); then
  echo "UNEXPECTED: generated runtime semantics accepted FloatV"
  exit 1
fi
echo "EXPECTED_DOMAIN_GAP: Python numeric inputs exist that the K runtime cannot execute"
exit 0
