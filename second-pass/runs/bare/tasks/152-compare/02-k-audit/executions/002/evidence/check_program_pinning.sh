#!/usr/bin/env bash
set -euo pipefail

cd /tmp/audit-work/152-compare

mpy_normalized="$(tr -d '[:space:]' < solution.mpy)"
rhs_normalized="$(
  sed -n '/rule solutionProgram =>/,/\/\/ Independent/p' verification.k |
    sed '1d;$d' |
    sed 's/\.Exprs//g; s/\.Stmts//g' |
    tr -d '[:space:]'
)"

printf '%s' "$mpy_normalized" | sha256sum
printf '%s' "$rhs_normalized" | sha256sum
test "$mpy_normalized" = "$rhs_normalized"
printf 'normalized_constructor_terms_equal=true\n'
