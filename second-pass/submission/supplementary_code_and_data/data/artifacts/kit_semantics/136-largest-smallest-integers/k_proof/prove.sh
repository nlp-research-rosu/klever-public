#!/usr/bin/env bash
set -euo pipefail

kompile --version
krun --version
kprove --version

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
python3 -m py_compile solution.py
cmp solution.mpy <(python3 py2mpy.py solution.py)

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun solution.mpy --definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled

kompile --backend haskell connection.k \
  --main-module CONNECTION \
  --syntax-module MPY-SYNTAX \
  --output-definition connection-kompiled
kprove connection-spec.k \
  --definition connection-kompiled \
  --spec-module CONNECTION-SPEC

kompile --backend haskell verification-core.k \
  --main-module VERIFICATION-CORE \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-core-kompiled
kprove loop-spec.k \
  --definition verification-core-kompiled \
  --spec-module LOOP-SPEC

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

if kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
then
  echo "ERROR: false-result mutation unexpectedly proved" >&2
  exit 1
else
  echo "EXPECTED FAILURE: false-result mutation was rejected"
fi

kompile --backend haskell body-mutation.k \
  --main-module BODY-MUTATION \
  --syntax-module MPY-SYNTAX \
  --output-definition body-mutation-kompiled
if kprove body-mutation-spec.k \
  --definition body-mutation-kompiled \
  --spec-module BODY-MUTATION-SPEC
then
  echo "ERROR: mutated body unexpectedly proved the correct result" >&2
  exit 1
else
  echo "EXPECTED FAILURE: mutated body was rejected"
fi

python3 differential_test.py
