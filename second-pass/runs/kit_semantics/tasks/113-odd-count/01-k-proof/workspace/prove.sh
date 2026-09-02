#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-smoke.py > concrete-smoke.mpy
python3 validation.py

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-smoke.mpy --definition runtime-kompiled > concrete-smoke.out
test "$(sed -n '/<k>/{n;s/[[:space:]]//g;p;q;}' concrete-smoke.out)" = ".K"
test "$(sed -n '/<exit-code>/{n;s/[[:space:]]//g;p;q;}' concrete-smoke.out)" = "0"
echo "KRUN_SMOKE_OK"

kompile --backend haskell reference-semantics/semantics.k \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition reference-proof-kompiled
kprove projection-spec.k \
  --definition reference-proof-kompiled \
  --spec-module PROJECTION-SPEC | tee projection-proof.out

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC | tee target-proof.out

if kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY > vacuity.out 2>&1
then
  echo "ERROR: false-result mutation unexpectedly proved"
  exit 1
else
  echo "EXPECTED_FAILURE false-result"
fi

if kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION > body-mutation.out 2>&1
then
  echo "ERROR: changed-body mutation unexpectedly proved"
  exit 1
else
  echo "EXPECTED_FAILURE changed-body"
fi

if kprove spec-count-mutation.k \
  --definition reference-proof-kompiled \
  --spec-module SPEC-COUNT-MUTATION > count-mutation.out 2>&1
then
  echo "ERROR: wrong-count mutation unexpectedly proved"
  exit 1
else
  echo "EXPECTED_FAILURE wrong-count"
fi
