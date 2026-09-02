#!/usr/bin/env bash
set -euxo pipefail

python3 py2mpy.py solution.py > solution.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete-tests.mpy \
  --definition runtime-kompiled \
  --output none

kompile verification.k \
  --backend haskell \
  --main-module MATCH-PARENS-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module MATCH-PARENS-SPEC \
  --claims loopCorrect \
  --output pretty

kprove spec.k \
  --definition verification-kompiled \
  --spec-module MATCH-PARENS-SPEC \
  --claims loopCorrect,loopFirstCorrect \
  --trusted loopCorrect \
  --output pretty

kprove spec.k \
  --definition verification-kompiled \
  --spec-module MATCH-PARENS-SPEC \
  --claims loopCorrect,loopFirstCorrect,isGoodCorrect \
  --trusted loopCorrect,loopFirstCorrect \
  --output pretty

kprove spec.k \
  --definition verification-kompiled \
  --spec-module MATCH-PARENS-SPEC \
  --claims goodBranchCorrect \
  --output pretty

kprove spec.k \
  --definition verification-kompiled \
  --spec-module MATCH-PARENS-SPEC \
  --claims loopCorrect,loopFirstCorrect,isGoodCorrect,goodBranchCorrect,matchParensCorrect \
  --trusted loopCorrect,loopFirstCorrect,isGoodCorrect,goodBranchCorrect \
  --output pretty
