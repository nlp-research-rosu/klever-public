#!/usr/bin/env bash
set -euo pipefail

cd /tmp/audit-work/fresh
audit_index=0
for audit_input in "" "a" "a a b" "a b b" "a a b b c"; do
  audit_index=$((audit_index + 1))
  audit_k_string="\"${audit_input}\""
  audit_fixed="/tmp/audit-work/bridge-fixed-${audit_index}.txt"
  audit_extended="/tmp/audit-work/bridge-extended-${audit_index}.txt"
  printf 'INPUT=%q\n' "$audit_input"
  printf 'COMMAND=krun solution.mpy --definition verification-haskell-kompiled -cTEST=%q --output pretty\n' "$audit_k_string"
  krun solution.mpy --definition verification-haskell-kompiled -cTEST="$audit_k_string" --output pretty > "$audit_fixed"
  printf 'COMMAND=krun solution.mpy --definition lemmas-haskell-kompiled -cTEST=%q --output pretty\n' "$audit_k_string"
  krun solution.mpy --definition lemmas-haskell-kompiled -cTEST="$audit_k_string" --output pretty > "$audit_extended"
  printf 'FIXED_OUTPUT\n'
  sed -n '1,40p' "$audit_fixed"
  printf 'EXTENDED_OUTPUT\n'
  sed -n '1,40p' "$audit_extended"
  cmp -s "$audit_fixed" "$audit_extended"
  printf 'BYTE_IDENTICAL=true\n'
done
