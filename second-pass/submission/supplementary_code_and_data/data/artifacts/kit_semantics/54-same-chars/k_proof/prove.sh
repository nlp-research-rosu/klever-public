#!/usr/bin/env bash
set -eu

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py krun-smoke.py > krun-smoke.mpy
python3 -m py_compile solution.py test_solution.py
python3 test_solution.py

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun solution.mpy --definition runtime-kompiled
krun krun-smoke.mpy --definition runtime-kompiled

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
  echo "ERROR: the false-postcondition mutation unexpectedly passed"
  exit 1
else
  vacuity_exit=$?
  echo "EXPECTED_FAILURE: spec-vacuity.k exited ${vacuity_exit}"
fi

if kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
then
  echo "ERROR: the changed-body mutation unexpectedly passed"
  exit 1
else
  body_mutation_exit=$?
  echo "EXPECTED_FAILURE: spec-body-mutation.k exited ${body_mutation_exit}"
fi
