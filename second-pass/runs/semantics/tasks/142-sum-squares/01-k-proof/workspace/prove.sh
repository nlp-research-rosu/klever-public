#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Translate the submitted implementation with the fixed frontend.
python3 py2mpy.py solution.py > solution.mpy

# Compile and exercise the supplied concrete semantics.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
krun concrete_tests.mpy \
  --definition runtime-kompiled \
  --output pretty

# Compile the symbolic definition.  SUM-SQUARES-VERIFICATION imports MPY,
# deliberately excluding the concrete-only MPY-CONCRETE module.
kompile verification.k \
  --backend haskell \
  --main-module SUM-SQUARES-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

# Prove the induction lemma without assumptions.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SUM-SQUARES-SPEC \
  --claims SUM-SQUARES-SPEC.loop \
  --output pretty

# Prove the body summary, admitting only the lemma just proved.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SUM-SQUARES-SPEC \
  --claims SUM-SQUARES-SPEC.body,SUM-SQUARES-SPEC.loop \
  --trusted SUM-SQUARES-SPEC.loop \
  --output pretty

# Prove the end-to-end call, admitting only the body summary just proved.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SUM-SQUARES-SPEC \
  --claims SUM-SQUARES-SPEC.main,SUM-SQUARES-SPEC.body \
  --trusted SUM-SQUARES-SPEC.body \
  --output pretty
