#!/usr/bin/env bash
set -euo pipefail

export PATH="$HOME/.nix-profile/bin:$PATH"

python3 py2mpy.py solution.py > solution.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

python3 py2mpy.py smoke.py > smoke.mpy
krun smoke.mpy --definition runtime-kompiled
python3 differential_test.py

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

# Prove the exact loop-tail connection theorem without assuming it.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-invariant

# Use that separately proved connection theorem as a trusted circularity while
# proving the entry-point claim. Both positive commands must print #Top.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --trusted SPEC.loop-invariant

# Gate A5: the deliberately false [] -> [0] result must be rejected.
if kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY 2>&1 | tee vacuity.log; then
  echo "UNEXPECTED SUCCESS: false-result mutation proved"
  exit 1
else
  echo "EXPECTED FAILURE: false-result mutation rejected"
fi

# Gate A1: the changed second append must invalidate the original result.
if kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION 2>&1 | tee body-mutation.log; then
  echo "UNEXPECTED SUCCESS: changed-body mutation proved"
  exit 1
else
  echo "EXPECTED FAILURE: changed-body mutation rejected"
fi
