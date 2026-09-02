#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke-empty.py > smoke-empty.mpy
python3 py2mpy.py smoke.py > smoke.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun smoke-empty.mpy --definition runtime-kompiled

if krun smoke.mpy --definition runtime-kompiled; then
  echo "UNEXPECTED: opaque nonempty MD5 execution succeeded under LLVM"
  exit 1
else
  llvm_probe_rc=$?
  echo "EXPECTED_OPAQUE_LLVM_FAILURE exit=$llvm_probe_rc"
fi

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

krun smoke.mpy --definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.empty-input

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.nonempty-input

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

if kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
then
  echo "UNEXPECTED: false postcondition was proved"
  exit 1
else
  vacuity_probe_rc=$?
  echo "EXPECTED_VACUITY_FAILURE exit=$vacuity_probe_rc"
fi

if kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
then
  echo "UNEXPECTED: mutated function body satisfied the original result"
  exit 1
else
  body_probe_rc=$?
  echo "EXPECTED_BODY_MUTATION_FAILURE exit=$body_probe_rc"
fi

python3 test_solution.py
