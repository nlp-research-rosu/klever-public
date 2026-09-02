#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy

# verification.k's solutionProgram is the exact AST term with this digest.
printf '%s  %s\n' \
  '811ba0bc5a0aa8ce22bfa580e3e6d165e2638b036e676be0f25b8a4acf753125' \
  'solution.mpy' \
  | sha256sum --check -

rm -rf -- ./runtime-kompiled ./verification-kompiled

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete_tests.mpy \
  --definition runtime-kompiled \
  --output pretty

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled \
  -I .

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --output pretty
