#!/usr/bin/env bash
set -euo pipefail

# Recreate the required transliteration and ensure the concrete driver embeds
# exactly the implementation from solution.py.
python3 py2mpy.py solution.py > solution.mpy
sed -n '1,2p' concrete_tests.py | diff -u solution.py -
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy

# Concrete execution under the required LLVM main and syntax modules.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_tests.mpy --definition runtime-kompiled

# Symbolic proof. VERIFICATION imports MPY, which deliberately excludes the
# concrete-only MPY-CONCRETE extension.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
