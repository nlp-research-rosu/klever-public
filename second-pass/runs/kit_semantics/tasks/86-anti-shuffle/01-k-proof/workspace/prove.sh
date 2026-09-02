#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
python3 generate_program_module.py

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled

kompile --backend haskell reference-semantics/semantics.k \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition lemma-kompiled
kprove lemma-spec.k \
  --definition lemma-kompiled \
  --spec-module LEMMA-SPEC

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

python3 test_solution.py

if kprove spec-vacuity.k \
    --definition verification-kompiled \
    --spec-module SPEC-VACUITY \
    > vacuity.log 2>&1; then
  cat vacuity.log
  echo "UNEXPECTED: false-result vacuity claim proved" >&2
  exit 1
else
  cat vacuity.log
  echo "EXPECTED FAILURE: false-result vacuity claim was rejected"
fi

./mutation-probe.sh
