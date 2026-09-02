#!/usr/bin/env bash
set -eu

# Translate the submitted implementation.
python3 py2mpy.py solution.py > solution.mpy

# Concrete execution with the supplied LLVM semantics.
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
python3 make_smoke.py 0 > smoke-0.mpy
python3 make_smoke.py 5 > smoke-5.mpy
krun smoke-0.mpy --definition runtime-kompiled --output pretty > smoke-0.out
krun smoke-5.mpy --definition runtime-kompiled --output pretty > smoke-5.out
rg -F '0 |-> list ( .ValSeq )' smoke-0.out
rg -F '0 |-> list ( vCons ( 1 , vCons ( 2 , vCons ( 6 , vCons ( 24 , vCons ( 15 , .ValSeq ) ) ) ) ) )' smoke-5.out

# Independent finite differential check against the prompt-level formula.
python3 test_solution.py

# Symbolic definition and all positive target claims.
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

# Gate A5: deliberately false final result. The proof must reject it.
sed \
  -e 's/module SPEC/module SPEC-VACUITY/' \
  -e 's/list(resultRun(.ValSeq, 1, N, 1, 0))/list(vCons(999, resultRun(.ValSeq, 1, N, 1, 0)))/' \
  spec.k > spec-vacuity.k
if kprove spec-vacuity.k \
     --definition verification-kompiled \
     --spec-module SPEC-VACUITY > spec-vacuity.out 2>&1; then
  echo "ERROR: false-postcondition mutation unexpectedly proved" >&2
  exit 1
else
  mutation_status=$?
  rg -m 1 'WarnStuckClaimState' spec-vacuity.out
  echo "EXPECTED FAILURE: false-postcondition exit ${mutation_status}"
fi

# Gate A1: a material source-body change must invalidate the connection proof.
sed \
  -e 's/module SPEC/module SPEC-BODY-MUTATION/' \
  -e 's/Assign(Name("total"), Int(0))/Assign(Name("total"), Int(100))/' \
  spec.k > spec-body-mutation.k
if kprove spec-body-mutation.k \
     --definition verification-kompiled \
     --spec-module SPEC-BODY-MUTATION > spec-body-mutation.out 2>&1; then
  echo "ERROR: body mutation unexpectedly proved" >&2
  exit 1
else
  body_status=$?
  rg -m 1 'WarnStuckClaimState' spec-body-mutation.out
  echo "EXPECTED FAILURE: body-mutation exit ${body_status}"
fi
