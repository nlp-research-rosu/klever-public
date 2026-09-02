#!/usr/bin/env bash
set -euo pipefail

# Recreate the required constructor term and check that the concrete harness
# contains the exact same implementation before its assertions.
python3 -m py_compile solution.py
python3 py2mpy.py solution.py > solution.mpy
diff -u solution.py <(sed -n '1,3p' concrete-tests.py)
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy

# Concrete execution uses the required LLVM main and syntax modules.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy \
  --definition runtime-kompiled \
  --output pretty | tee concrete-run.out
rg -U -q '<exc>[[:space:]]+NoExc[[:space:]]+</exc>' concrete-run.out
rg -U -q '<exit-code>[[:space:]]+0[[:space:]]+</exit-code>' concrete-run.out

# Symbolic verification imports MPY (not MPY-KRUN/MPY-CONCRETE).
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC | tee kprove.out
test "$(tr -d '\r\n' < kprove.out)" = '#Top'
