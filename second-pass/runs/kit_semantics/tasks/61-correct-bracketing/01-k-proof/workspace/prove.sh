#!/usr/bin/env bash
set -euo pipefail

echo "== Translate and check the exact solution =="
cmp solution.mpy <(python3 py2mpy.py solution.py)
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
python3 py2mpy.py bridge_context_tests.py > bridge_context_tests.mpy
python3 differential_test.py

echo "== Compile the supplied semantics for concrete LLVM execution =="
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

echo "== Exercise the exact implementation concretely =="
CONCRETE_RESULT="$(krun concrete_tests.mpy --definition runtime-kompiled)"
grep -F '"case_empty" |-> true' <<<"$CONCRETE_RESULT"
grep -F '"case_open" |-> false' <<<"$CONCRETE_RESULT"
grep -F '"case_pair" |-> true' <<<"$CONCRETE_RESULT"
grep -F '"case_nested" |-> true' <<<"$CONCRETE_RESULT"
grep -F '"case_bad_prefix" |-> false' <<<"$CONCRETE_RESULT"

echo "== Compile the bridge-free symbolic definition =="
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

echo "== Positive proof 1: universal loop theorem, bridge-free =="
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop

echo "== Compile the proved loop theorem as an exact operational lemma =="
kompile verification-with-loop.k \
  --backend haskell \
  --main-module VERIFICATION-WITH-LOOP \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-with-loop-kompiled

echo "== Positive proof 2: exact whole-program entry theorem =="
kprove spec.k \
  --definition verification-with-loop-kompiled \
  --spec-module SPEC \
  --claims SPEC.correct-bracketing

echo "== Fixed-versus-bridge complete-state and context-containment checks =="
FIXED_CONTEXT="$(krun bridge_context_tests.mpy --definition runtime-kompiled)"
BRIDGE_CONTEXT="$(
  krun bridge_context_tests.mpy --definition verification-with-loop-kompiled
)"
test "$FIXED_CONTEXT" = "$BRIDGE_CONTEXT"
grep -F '"context_result" |-> false' <<<"$FIXED_CONTEXT"

echo "== Expected failure: false whole-program result =="
if kprove spec-vacuity.k \
  --definition verification-with-loop-kompiled \
  --spec-module SPEC-VACUITY
then
  echo "ERROR: false postcondition unexpectedly proved"
  exit 1
else
  VACUITY_STATUS=$?
  echo "EXPECTED FAILURE exit=$VACUITY_STATUS"
fi

echo "== Expected failure: opposite bridge value =="
if kprove spec-value-mutation.k \
  --definition verification-with-loop-kompiled \
  --spec-module SPEC-VALUE-MUTATION
then
  echo "ERROR: opposite bridge value unexpectedly proved"
  exit 1
else
  VALUE_STATUS=$?
  echo "EXPECTED FAILURE exit=$VALUE_STATUS"
fi

echo "== Expected failure: mutated source body breaks the connection theorem =="
if kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
then
  echo "ERROR: mutated body unexpectedly proved"
  exit 1
else
  BODY_STATUS=$?
  echo "EXPECTED FAILURE exit=$BODY_STATUS"
fi
