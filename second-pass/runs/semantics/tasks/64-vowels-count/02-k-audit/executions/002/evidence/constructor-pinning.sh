#!/usr/bin/env bash
set -u

cd /tmp/audit-work/proof || exit 1

kast ./solution.mpy \
  --definition ./proof-base-kompiled \
  --module VOWELS-BASE \
  --sort Module \
  --expand-macros \
  --output kore \
  --output-file ./solution.expanded.kore
solution_status=$?

kast \
  --expression vowelsModule \
  --definition ./proof-base-kompiled \
  --module VOWELS-BASE \
  --sort Module \
  --expand-macros \
  --output kore \
  --output-file ./macro.expanded.kore
macro_status=$?

printf 'solution_kast_exit=%d\n' "$solution_status"
printf 'macro_kast_exit=%d\n' "$macro_status"
sha256sum ./solution.expanded.kore ./macro.expanded.kore
cmp -s ./solution.expanded.kore ./macro.expanded.kore
cmp_status=$?
printf 'constructor_cmp_exit=%d\n' "$cmp_status"
if (( cmp_status != 0 )); then
  diff -u ./solution.expanded.kore ./macro.expanded.kore
fi

if (( solution_status != 0 )); then
  exit "$solution_status"
fi
if (( macro_status != 0 )); then
  exit "$macro_status"
fi
exit "$cmp_status"
