#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun solution.mpy --definition runtime-kompiled
krun concrete_tests.mpy --definition runtime-kompiled

kompile verification.k \
  --backend haskell \
  --main-module PLUCK-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition proof-kompiled

# First prove the induction lemma over the arbitrary input tail.
kprove spec.k \
  --definition proof-kompiled \
  --spec-module PLUCK-SPEC \
  --claims PLUCK-SPEC.pluck-loop \
  --output pretty

# Then prove module loading, call/return, and the result contract, using only
# the induction lemma proved by the preceding command as a trusted dependency.
kprove spec.k \
  --definition proof-kompiled \
  --spec-module PLUCK-SPEC \
  --claims PLUCK-SPEC.pluck-correct,PLUCK-SPEC.pluck-loop \
  --trusted PLUCK-SPEC.pluck-loop \
  --output pretty
