#!/usr/bin/env bash
set -euo pipefail

# Regenerate the required translation from the submitted Python source.
python3 py2mpy.py solution.py > solution.mpy

# Build and exercise the unmodified reference semantics concretely.
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_tests.mpy \
  --definition runtime-kompiled \
  | tee concrete-run.out
grep -A 1 '<exc>' concrete-run.out | grep -q 'NoExc'
grep -A 2 '<exit-code>' concrete-run.out | grep -q '    0'

# Build the proof definition from MPY (not MPY-KRUN/MPY-CONCRETE), then prove
# every claim in spec.k.  Success prints #Top and exits zero.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  | tee kprove.out
grep -qx '#Top' kprove.out
