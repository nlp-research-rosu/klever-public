#!/usr/bin/env bash
set -eu

# Generate the exact K constructor term from the submitted implementation.
python3 py2mpy.py solution.py > solution.mpy

# Independent finite differential evidence against brute-force enumeration.
python3 differential_test.py

# Concrete K execution of the example and boundary/representative cases.
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled

# Symbolic definition and positive target proofs.
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-invariant
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

# Gate A5: the concrete false result must not prove.
set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
vacuity_status=$?
set -e
printf 'spec-vacuity.k exit: %s (expected non-zero)\n' "$vacuity_status"
test "$vacuity_status" -ne 0

# Gate A1: a materially changed function body must not prove the old result.
set +e
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
body_mutation_status=$?
set -e
printf 'spec-body-mutation.k exit: %s (expected non-zero)\n' \
  "$body_mutation_status"
test "$body_mutation_status" -ne 0
