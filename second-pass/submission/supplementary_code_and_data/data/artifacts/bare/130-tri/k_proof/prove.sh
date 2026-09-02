#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

python3 py2mpy.py solution.py > solution.mpy

kompile verification.k \
  --backend haskell \
  --main-module TRI-VERIFICATION \
  --syntax-module MPY-SYNTAX

# Check that the program term used by the symbolic claims is byte-for-byte the
# same canonical KORE tree as the freshly translated solution.mpy.
translated_ast="$(
  kast --definition verification-kompiled \
    --module MPY-SYNTAX --sort Program --output kore solution.mpy
)"
proved_ast="$(
  kast --definition verification-kompiled \
    --module TRI-VERIFICATION --sort Program --expand-macros --output kore \
    --expression solutionProgram
)"
test "$translated_ast" = "$proved_ast"

krun solution.mpy -cN=0 --definition verification-kompiled
krun solution.mpy -cN=3 --definition verification-kompiled
krun solution.mpy -cN=6 --definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module TRI-SPEC
