#!/usr/bin/env bash
set -euo pipefail

# Regenerate the required constructor term from the submitted implementation.
python3 py2mpy.py solution.py > solution.mpy

# The concrete harness begins with an exact copy of solution.py.
diff -u solution.py <(sed -n '1,22p' concrete-tests.py)
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy

# Concrete execution uses exactly the requested LLVM definition.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled

# Symbolic reachability proof imports MPY through verification.k.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled
