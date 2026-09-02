#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete-tests.mpy --definition runtime-kompiled \
  2>&1 | tee concrete-output.txt
rg -q '"example_empty" \\|-> 0' concrete-output.txt
rg -q '"example_single" \\|-> 3' concrete-output.txt
rg -q '"example_overlap" \\|-> 3' concrete-output.txt
rg -q '"empty_substring" \\|-> 4' concrete-output.txt

python3 validate.py 2>&1 | tee differential-output.txt

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-inv \
  2>&1 | tee loop-proof-output.txt
rg -q '^#Top$' loop-proof-output.txt

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  2>&1 | tee target-proof-output.txt
rg -q '^#Top$' target-proof-output.txt

if kprove spec-vacuity.k \
     --definition verification-kompiled \
     --spec-module SPEC-VACUITY \
     2>&1 | tee vacuity-output.txt; then
  echo "ERROR: false-result mutation unexpectedly proved"
  exit 1
else
  mutation_status=$?
  echo "EXPECTED_FAILURE_FALSE_RESULT_EXIT=$mutation_status"
fi

if kprove spec-body-mutation.k \
     --definition verification-kompiled \
     --spec-module SPEC-BODY-MUTATION \
     2>&1 | tee body-mutation-output.txt; then
  echo "ERROR: changed-body mutation unexpectedly proved"
  exit 1
else
  mutation_status=$?
  echo "EXPECTED_FAILURE_CHANGED_BODY_EXIT=$mutation_status"
fi

rg -U -q '<k>[[:space:]]*3 ~> \.K' vacuity-output.txt
rg -U -q '<k>[[:space:]]*4 ~> \.K' body-mutation-output.txt
