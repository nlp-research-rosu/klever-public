#!/usr/bin/env bash
set -euo pipefail

scratch_root=/tmp/audit-work/96-count-up-to

printf 'Local K source/helper inventory\n'
find "$scratch_root" -maxdepth 1 -type f -name '*.k' -printf '%f\n' | sort

for source in semantic.k verification.k spec.k; do
  printf '\nNUMBERED SOURCE: %s\n' "$source"
  nl -ba "$scratch_root/$source"
done

printf '\nDeclarations, configuration, rules, and claims\n'
rg -n \
  '^[[:space:]]*(syntax|configuration|rule|claim)|\[(function|total|functional|simplification|concrete|priority|owise|anywhere|macro|macro-rec|symbol|hook|trusted)' \
  "$scratch_root/semantic.k" \
  "$scratch_root/verification.k" \
  "$scratch_root/spec.k"

printf '\nSensitive attribute scan\n'
for token in function total functional simplification concrete priority opaque anywhere owise macro trusted; do
  printf '%s:\n' "$token"
  rg -n "$token" \
    "$scratch_root/semantic.k" \
    "$scratch_root/verification.k" \
    "$scratch_root/spec.k" || true
done

printf '\nConstructors used in submitted solution.mpy\n'
rg -o '[A-Za-z][A-Za-z0-9-]*[(]' "$scratch_root/solution.mpy" \
  | tr -d '(' | sort -u

printf '\nLiteral operators and identifiers used in submitted solution.mpy\n'
rg -o '"[^"]+"' "$scratch_root/solution.mpy" | sort -u
