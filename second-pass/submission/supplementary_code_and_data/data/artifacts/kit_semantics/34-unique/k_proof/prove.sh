#!/usr/bin/env bash
set -euo pipefail

# Translator identity and concrete execution.
python3 py2mpy.py solution.py > solution.mpy
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled

# Independent CPython oracle and matching LLVM cases.
python3 concrete_tests.py
python3 py2mpy.py concrete_tests_k.py > concrete-tests.mpy
krun concrete-tests.mpy --definition runtime-kompiled

# Stage 1: prove the membership connection without its bridge.
kompile --backend haskell verification.k \
  --main-module VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-base-kompiled
kprove spec.k \
  --definition verification-base-kompiled \
  --spec-module MEMBER-SPEC

# Stage 2: use only the proved membership bridge to prove the source loop.
kompile --backend haskell verification.k \
  --main-module VERIFICATION-MEMBER \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-member-kompiled
kprove spec.k \
  --definition verification-member-kompiled \
  --spec-module LOOP-SPEC

# Stage 3: use both proved bridges for the full unbounded-domain target.
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

# Fixed-versus-bridged value and continuation probes.
kprove bridge-probes.k \
  --definition verification-base-kompiled \
  --spec-module MEMBER-PROBE-BASE
kprove bridge-probes.k \
  --definition verification-member-kompiled \
  --spec-module MEMBER-PROBE-BRIDGED
kprove bridge-probes.k \
  --definition verification-member-kompiled \
  --spec-module LOOP-PROBE-FIXED
kprove bridge-probes.k \
  --definition verification-kompiled \
  --spec-module LOOP-PROBE-BRIDGED

# Reproducible witness for the symbolic/concrete numeric-equality boundary.
kprove model-boundary.k \
  --definition verification-base-kompiled \
  --spec-module MODEL-BOUNDARY

# Negative validation probes: both commands must fail.
set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY > vacuity.log 2>&1
vacuity_rc=$?
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION > body-mutation.log 2>&1
body_mutation_rc=$?
set -e

if [[ "$vacuity_rc" -eq 0 ]]; then
  echo "ERROR: false-result mutation unexpectedly proved"
  exit 1
fi
if [[ "$body_mutation_rc" -eq 0 ]]; then
  echo "ERROR: removed-append mutation unexpectedly proved"
  exit 1
fi

echo "EXPECTED_FAILURE spec-vacuity.k exit=$vacuity_rc"
echo "EXPECTED_FAILURE spec-body-mutation.k exit=$body_mutation_rc"
