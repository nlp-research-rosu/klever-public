#!/usr/bin/env bash
set -euo pipefail
export PS4='+ ${BASH_SOURCE##*/}:${LINENO}: '
set -x

cd /tmp/audit-work/reconstruction

timeout 1200 kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition reviewer-runtime-kompiled
echo "FRESH_LLVM_KOMPILE_EXIT=$?"

python3 /reference/py2mpy.py reviewer-smoke.py > reviewer-smoke.mpy
echo "REVIEWER_SMOKE_TRANSLATION_EXIT=$?"

timeout 300 krun reviewer-smoke.mpy \
  --definition reviewer-runtime-kompiled
echo "REVIEWER_SMOKE_KRUN_EXIT=$?"

timeout 1200 kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition reviewer-verification-kompiled
echo "FRESH_HASKELL_KOMPILE_EXIT=$?"

kast --definition reviewer-verification-kompiled \
  --module VERIFICATION-SYNTAX \
  --sort Module \
  --expand-macros \
  --output kore \
  --expression 'Module(FuncDef("count_up_to", Params("n"), countBody))' \
  > reviewer-proof-program.kore
echo "PROOF_PROGRAM_KAST_EXIT=$?"

kast --definition reviewer-verification-kompiled \
  --module MPY-SYNTAX \
  --sort Module \
  --expand-macros \
  --output kore \
  solution.regenerated.mpy \
  > reviewer-solution-program.kore
echo "REGENERATED_PROGRAM_KAST_EXIT=$?"

cmp reviewer-proof-program.kore reviewer-solution-program.kore
echo "CONSTRUCTOR_LEVEL_PROGRAM_IDENTITY_EXIT=$?"
sha256sum reviewer-proof-program.kore reviewer-solution-program.kore

timeout 1200 kprove spec.k \
  --definition reviewer-verification-kompiled \
  --spec-module SPEC
echo "ALL_POSITIVE_CLAIMS_KPROVE_EXIT=$?"
