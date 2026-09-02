#!/usr/bin/env bash
set -euo pipefail

scratch=/tmp/audit-work/review-43
cd "$scratch"

# Extract the generated FuncDef (dropping the outer Module close) and the
# FuncDef embedded in the entry claim.
sed -n '2,17p' regenerated-solution.mpy | sed '$s/)$//' \
  > generated-function.mpy
# Rule syntax writes empty statement sequences explicitly as `.Stmts`; program
# syntax writes the same unit as an omitted argument. Normalize only that unit.
sed -n '44,61p' spec.k | sed 's/\.Stmts//g' > claimed-function.mpy

kast generated-function.mpy \
  --definition review-verification-kompiled \
  --sort Stmt \
  --output kore \
  --output-file generated-function.kore

kast claimed-function.mpy \
  --definition review-verification-kompiled \
  --sort Stmt \
  --output kore \
  --output-file claimed-function.kore

sha256sum generated-function.mpy claimed-function.mpy
sha256sum generated-function.kore claimed-function.kore
cmp generated-function.kore claimed-function.kore
compare_exit=$?
echo "CONSTRUCTOR_COMPARE_EXIT=$compare_exit"
