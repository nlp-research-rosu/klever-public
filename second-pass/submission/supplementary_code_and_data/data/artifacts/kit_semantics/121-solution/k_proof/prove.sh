#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
python3 differential_test.py

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled

# Bridge-free universal connection theorem.
kompile --backend haskell verification-base.k \
  --main-module VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-base-kompiled
kprove connection-spec.k \
  --definition verification-base-kompiled \
  --spec-module CONNECTION-SPEC
kprove projection-positive.k \
  --definition verification-base-kompiled \
  --spec-module PROJECTION-POSITIVE

# Full non-empty symbolic target theorem.
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

# Negative validation probes must all be rejected.
if kprove spec-vacuity.k \
    --definition verification-kompiled \
    --spec-module SPEC-VACUITY; then
  echo "ERROR: false postcondition unexpectedly proved" >&2
  exit 1
else
  echo "EXPECTED FAILURE: false postcondition rejected"
fi

if kprove connection-mutation.k \
    --definition verification-base-kompiled \
    --spec-module CONNECTION-MUTATION; then
  echo "ERROR: mutated loop connection unexpectedly proved" >&2
  exit 1
else
  echo "EXPECTED FAILURE: mutated loop connection rejected"
fi

if kprove connection-mutation.k \
    --definition verification-kompiled \
    --spec-module CONNECTION-MUTATION; then
  echo "ERROR: loop bridge matched a mutated body" >&2
  exit 1
else
  echo "EXPECTED FAILURE: loop bridge rejected the mutated body"
fi

if kprove projection-mutation.k \
    --definition verification-base-kompiled \
    --spec-module PROJECTION-MUTATION; then
  echo "ERROR: false projection interpretation unexpectedly proved" >&2
  exit 1
else
  echo "EXPECTED FAILURE: false projection interpretation rejected"
fi
