#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Translate the submitted implementation.
python3 py2mpy.py solution.py > solution.mpy

# Build and exercise the required concrete LLVM semantics.  Assertion failure
# sets the semantics' exit code to 1, so set -e makes this a hard failure.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

{
  sed -n '1,$p' solution.py
  printf '%s\n' \
    'assert f(0) == []' \
    'assert f(1) == [1]' \
    'assert f(5) == [1, 2, 6, 24, 15]' \
    'assert f(8) == [1, 2, 6, 24, 15, 720, 28, 40320]'
} | python3 py2mpy.py /dev/stdin \
  | krun /dev/stdin --definition runtime-kompiled --output pretty

# Build the symbolic definition from MPY (not MPY-KRUN).
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

# First discharge the loop theorem.  Then use that proved theorem as a lemma
# for the complete symbolic function-call claim.  The final command proves
# both independent end-to-end concrete claims.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims loop-correct

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims loop-correct,f-symbolic \
  --trusted loop-correct

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims f-zero,f-five
