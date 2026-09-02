#!/usr/bin/env bash
set -euo pipefail

cd /tmp/audit-work/fresh-k-001

solution_command=(
  kast solution.mpy
  --definition verification-kompiled
  --module VERIFICATION
  --sort Module
  --expand-macros
  --output kore
)
macro_command=(
  kast
  --expression '#solutionModule'
  --definition verification-kompiled
  --module VERIFICATION
  --sort Module
  --expand-macros
  --output kore
)

printf 'SOLUTION_COMMAND:'
printf ' %q' "${solution_command[@]}"
printf '\nMACRO_COMMAND:'
printf ' %q' "${macro_command[@]}"
printf '\n'

printf 'SOLUTION_AST_SHA256  '
"${solution_command[@]}" | sha256sum
printf 'MACRO_AST_SHA256     '
"${macro_command[@]}" | sha256sum

diff -u <("${solution_command[@]}") <("${macro_command[@]}")
printf 'EXPANDED_AST_IDENTITY=PASS\n'
