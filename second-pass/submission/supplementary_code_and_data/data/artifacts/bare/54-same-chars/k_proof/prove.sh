#!/usr/bin/env bash
set -euo pipefail

cd -- "$(dirname -- "$0")"

# Translate the submitted Python and make that exact constructor term available
# to the K claims as solutionProgram.
python3 py2mpy.py solution.py > solution.mpy
python3 embed_mpy.py solution.mpy > solution-program.k

# Compile the handwritten semantics together with the generated program and
# the independently named contract predicate.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX

# Exercise the translated artifact through both result branches.
krun solution.mpy \
  --definition verification-kompiled \
  -cS0='"eabcdzzzz"' \
  -cS1='"dddzzzzzzzddeddabc"'
krun solution.mpy \
  --definition verification-kompiled \
  -cS0='"eabcd"' \
  -cS1='"dddddddabc"'

# Prove the universal theorem and every prompt-example claim.
kprove spec.k --definition verification-kompiled
