#!/usr/bin/env bash
set -euo pipefail

# Translate the submitted implementation with the fixed front end.
python3 py2mpy.py solution.py > solution.mpy
python3 -m py_compile solution.py

# Independent finite differential evidence and an AST identity check for the
# function copied into the concrete K test module.
python3 test_solution.py
python3 py2mpy.py krun_examples.py > krun_examples.mpy

# Gate C concrete execution uses exactly the requested LLVM main/syntax modules.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun krun_examples.mpy --definition runtime-kompiled

# Positive symbolic target proof.
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.bf-correct

# Gate A5: a deliberately false postcondition must not prove.
if kprove spec-vacuity.k \
     --definition verification-kompiled \
     --spec-module SPEC-VACUITY > vacuity.out 2>&1; then
  cat vacuity.out
  echo "ERROR: false-postcondition mutation unexpectedly proved" >&2
  exit 1
else
  status=$?
  cat vacuity.out
  echo "VACUITY_EXIT=$status"
fi

# Gate A1: a material body mutation must invalidate the original property.
kompile --backend haskell verification-mutant.k \
  --main-module MUTATION \
  --syntax-module MPY-SYNTAX \
  --output-definition mutation-kompiled
if kprove spec-body-mutation.k \
     --definition mutation-kompiled \
     --spec-module SPEC-BODY-MUTATION > body-mutation.out 2>&1; then
  cat body-mutation.out
  echo "ERROR: changed-body mutation unexpectedly proved" >&2
  exit 1
else
  status=$?
  cat body-mutation.out
  echo "BODY_MUTATION_EXIT=$status"
fi
