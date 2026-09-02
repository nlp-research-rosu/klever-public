#!/usr/bin/env bash
set -euo pipefail

# Translate and check the final Python implementation.
python3 py2mpy.py solution.py > solution.mpy
python3 -m py_compile solution.py
python3 differential_test.py

# Concrete execution under the required LLVM main module.
python3 py2mpy.py smoke.py > smoke.mpy
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled --output none

# Symbolic proof: this single command proves every claim in SPEC together,
# keeping the loop invariant available to the entry claim as a circularity.
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

# Gate A5: deliberately negate the summary in the target postcondition.
sed \
  -e 's/module SPEC/module SPEC-VACUITY/' \
  -e 's/andBool scanHappy(IS, 0, -1, -1))/andBool notBool scanHappy(IS, 0, -1, -1))/' \
  spec.k > spec-vacuity.k
set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
vacuity_exit=$?
set -e
printf 'spec-vacuity exit: %s (expected nonzero)\n' "$vacuity_exit"
if [[ "$vacuity_exit" -eq 0 ]]; then
  echo "ERROR: false-postcondition mutation unexpectedly proved"
  exit 1
fi

# Gate A1: materially mutate the embedded function body.
sed \
  '0,/Assign(Name("happy"), Bool(true))/s//Assign(Name("happy"), Bool(false))/' \
  spec.k > spec-body-mutation.k
set +e
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC
body_exit=$?
set -e
printf 'spec-body-mutation exit: %s (expected nonzero)\n' "$body_exit"
if [[ "$body_exit" -eq 0 ]]; then
  echo "ERROR: body mutation unexpectedly proved"
  exit 1
fi
