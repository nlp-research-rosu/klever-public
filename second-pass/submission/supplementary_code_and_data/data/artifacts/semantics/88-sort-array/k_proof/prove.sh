#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Rebuild both translated programs and ensure the concrete harness contains
# the submitted implementation verbatim.
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
diff -u solution.py <(head -n "$(wc -l < solution.py)" concrete_tests.py)

# Concrete execution uses the required LLVM entry module.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_tests.mpy --definition runtime-kompiled

# Symbolic verification imports MPY, without the concrete-only extension.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
