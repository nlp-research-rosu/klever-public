#!/bin/sh
set -eu

# Recreate the translated program.
python3 py2mpy.py solution.py > solution.mpy

# Concrete execution under the required LLVM main and syntax modules.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
python3 py2mpy.py smoke.py > smoke.mpy
krun smoke.mpy --definition runtime-kompiled
python3 differential_test.py

# Bridge-free connection proof: VERIFICATION-BASE does not import the guarded
# dynamic-dispatch simplification rule in module VERIFICATION.
kompile --backend haskell verification.k \
  --main-module VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition connection-kompiled
kprove spec-connection.k \
  --definition connection-kompiled \
  --spec-module SPEC-CONNECTION

# Required unbounded target proof.
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.filter-loop
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

# Gate A5: the deliberately false result must not prove.
if kprove spec-vacuity.k \
    --definition verification-kompiled \
    --spec-module SPEC-VACUITY
then
  echo "ERROR: false-result mutation unexpectedly proved" >&2
  exit 1
else
  echo "EXPECTED FAILURE: false-result mutation rejected"
fi

# Gate A1: removing append from the body must invalidate the result claim.
if kprove spec-body-mutation.k \
    --definition verification-kompiled \
    --spec-module SPEC-BODY-MUTATION
then
  echo "ERROR: body mutation unexpectedly proved" >&2
  exit 1
else
  echo "EXPECTED FAILURE: removed-append mutation rejected"
fi
