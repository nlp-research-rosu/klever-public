#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Translate the submitted implementation and ensure the proof's reviewed K
# rendering still corresponds exactly to it.
python3 py2mpy.py solution.py > solution.mpy
sha256sum solution.mpy | grep -q \
  '^39fcb6e88010732b87b6c5dee672f79d7d5b9e807254fb8074454cc36ed79662  solution.mpy$'

# Execute the examples and additional duplicate/tie/empty cases with the LLVM
# concrete semantics requested by the task.
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_tests.mpy \
  --definition runtime-kompiled \
  --output pretty > concrete-run.out
grep -A 2 '<exc>' concrete-run.out | grep -q 'NoExc'
grep -A 2 '<exit-code>' concrete-run.out | grep -q '0'

# Build the proof-only definition by importing MPY (not MPY-KRUN), then prove
# every claim in HUMANEVAL-SPEC.
kompile verification.k \
  --backend haskell \
  --main-module HUMANEVAL-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module HUMANEVAL-SPEC | tee kprove.out
grep -qx '#Top' kprove.out
