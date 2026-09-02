#!/usr/bin/env bash
set -euo pipefail

definition=/tmp/audit-work/int-oracle-kompiled
cases=(
  'evalInt(7 -Int 12)'
  'evalInt(7 +Int -12)'
  'evalInt(-7 *Int -3)'
  'evalBool(false andBool true)'
  'evalBool(true andBool false)'
  'evalBool(true andBool true)'
  'evalBool(-7 <Int -6)'
  'evalBool(-7 <Int -7)'
  'evalBool(-7 <=Int -7)'
  'evalInt(-7 %Int 10)'
  'evalInt(-13 %Int 10)'
  'evalInt(13 %Int 10)'
  'evalInt(-7 /Int 10)'
  'evalInt(-13 /Int 10)'
  'evalInt(13 /Int 10)'
)

for expression in "${cases[@]}"; do
  printf 'COMMAND: krun -d %s -cPGM=%q --output pretty\n' \
    "$definition" "$expression"
  krun -d "$definition" -cPGM="$expression" --output pretty
done
