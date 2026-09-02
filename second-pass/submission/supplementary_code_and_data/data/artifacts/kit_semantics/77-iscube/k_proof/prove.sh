#!/usr/bin/env bash
set -euo pipefail

python3 -m py_compile solution.py
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py solution.py | diff -u solution.mpy -

python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
sed -n '1,9p' concrete_tests.py | diff -u solution.py -

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete_tests.mpy --definition runtime-kompiled

kompile --backend haskell verification-base.k \
  --main-module VERIFICATION-BASE \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-base-kompiled

kprove identity-spec.k \
  --definition verification-base-kompiled \
  --spec-module IDENTITY

kprove connection-spec.k \
  --definition verification-base-kompiled \
  --spec-module CONNECTION

kompile --backend haskell connection-rule.k \
  --main-module CONNECTION-RULE \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition connection-rule-kompiled

kprove source-connection-spec.k \
  --definition connection-rule-kompiled \
  --spec-module SOURCE-CONNECTION

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

kprove ground-value-spec.k \
  --definition verification-kompiled \
  --spec-module GROUND-VALUES

# Fixed-semantics versus bridge-enabled comparisons over the bridge domains.
kprove connection-spec.k \
  --definition verification-kompiled \
  --spec-module CONNECTION \
  --depth 1

if kprove identity-mutation-spec.k \
     --definition verification-base-kompiled \
     --spec-module IDENTITY-MUTATION \
     > identity-mutation.log 2>&1; then
  echo "UNEXPECTED SUCCESS: identity mutation"
  exit 1
else
  identity_status=$?
  sed -n '1,80p' identity-mutation.log
  printf 'EXPECTED FAILURE: identity mutation exit %s\n' "$identity_status"
fi

if kprove connection-mutation-spec.k \
     --definition verification-base-kompiled \
     --spec-module CONNECTION-MUTATION \
     > connection-mutation.log 2>&1; then
  echo "UNEXPECTED SUCCESS: connection mutation"
  exit 1
else
  connection_status=$?
  sed -n '1,80p' connection-mutation.log
  printf 'EXPECTED FAILURE: connection mutation exit %s\n' "$connection_status"
fi

if kprove bridge-context-probe.k \
     --definition verification-kompiled \
     --spec-module BRIDGE-CONTEXT-PROBE \
     --depth 1 \
     > bridge-context-probe.log 2>&1; then
  echo "UNEXPECTED SUCCESS: widened bridge context"
  exit 1
else
  context_status=$?
  sed -n '1,80p' bridge-context-probe.log
  printf 'EXPECTED FAILURE: widened bridge context exit %s\n' "$context_status"
fi

if kprove spec-vacuity.k \
     --definition verification-kompiled \
     --spec-module SPEC-VACUITY \
     > spec-vacuity.log 2>&1; then
  echo "UNEXPECTED SUCCESS: false postcondition"
  exit 1
else
  vacuity_status=$?
  sed -n '1,80p' spec-vacuity.log
  printf 'EXPECTED FAILURE: false postcondition exit %s\n' "$vacuity_status"
fi

python3 differential_test.py
