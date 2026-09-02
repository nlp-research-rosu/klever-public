#!/usr/bin/env bash
set -e
set -u
set -o pipefail
PS4='+ ${BASH_SOURCE}:${LINENO}: '
set -x

# Lines 9--67 are the complete Pgm right-hand side of solutionProgram.
sed -n '9,67p' verification.k > extracted-solution-program.mpy
# `.Stmts` is K's internal empty-list spelling inside a rule; the concrete
# MPY surface syntax represents that same list with no token.
sed -i 's/\.Stmts//g' extracted-solution-program.mpy

kast submitted-solution.mpy \
  --definition audit-verification-kompiled \
  --sort Pgm --output kore > submitted-solution.kore
kast extracted-solution-program.mpy \
  --definition audit-verification-kompiled \
  --sort Pgm --output kore > verification-solution.kore

cmp submitted-solution.kore verification-solution.kore
sha256sum \
  submitted-solution.mpy extracted-solution-program.mpy \
  submitted-solution.kore verification-solution.kore
printf 'structural_kore_identity=yes\n'
