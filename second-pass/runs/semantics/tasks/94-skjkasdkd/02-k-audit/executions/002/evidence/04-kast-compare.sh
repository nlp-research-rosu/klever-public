#!/usr/bin/env bash
set -u

definition=/tmp/audit-work/reconstruction/reviewer-verification-kompiled
work=/tmp/audit-work/reconstruction

echo "COMMAND: kast exact submitted solution.mpy with macros expanded"
kast \
  --definition "$definition" \
  --module VERIFICATION \
  --sort Module \
  --expand-macros \
  --output kore \
  "$work/solution.mpy" \
  --output-file "$work/solution.kore"
solution_rc=$?
echo "solution_kast_status=$solution_rc"

echo "COMMAND: kast solutionModule proof symbol with macros expanded"
kast \
  --definition "$definition" \
  --module VERIFICATION \
  --sort Module \
  --expand-macros \
  --output kore \
  "$work/solution-module-symbol.mpy" \
  --output-file "$work/solution-module-symbol.kore"
symbol_rc=$?
echo "symbol_kast_status=$symbol_rc"

echo "COMMAND: cmp expanded KORE constructor terms"
cmp "$work/solution.kore" "$work/solution-module-symbol.kore"
cmp_rc=$?
echo "constructor_cmp_status=$cmp_rc"

echo "COMMAND: sha256sum expanded KORE terms"
sha256sum "$work/solution.kore" "$work/solution-module-symbol.kore"

if (( solution_rc || symbol_rc || cmp_rc )); then
  exit 1
fi
