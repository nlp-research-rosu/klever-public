#!/usr/bin/env bash
set -euo pipefail

# Translate and sanity-check the submitted implementation.
python3 py2mpy.py solution.py > solution.mpy
python3 -m py_compile solution.py

# Compile exactly the supplied concrete semantics and exercise the program.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
krun concrete_tests.mpy --definition runtime-kompiled

# Compile the proof definition, which imports MPY without concrete extensions,
# and prove every claim in FILTER-SPEC in one positive target-proof command.
kompile verification.k \
  --backend haskell \
  --main-module FILTER-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module FILTER-SPEC
