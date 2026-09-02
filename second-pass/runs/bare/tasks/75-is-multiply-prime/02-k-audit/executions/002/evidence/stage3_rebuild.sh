#!/usr/bin/env bash
set -euxo pipefail

cd /tmp/audit-work/75-is-multiply-prime/work

command -v kompile
command -v krun
command -v kprove
kompile --version
kprove --version

# This must print nothing: the scratch copy contains no candidate build/cache.
find . -maxdepth 1 -type d -name '*-kompiled' -print

# Fresh executable generated semantics.
kompile semantic.k \
  --backend llvm \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition concrete-kompiled

# Fresh proof definition. This includes the generated semantics and local
# verification helper from source, never a candidate-provided compiled tree.
kompile definition.k \
  --backend haskell \
  --main-module DEFINITION \
  --syntax-module MPY-SYNTAX \
  --output-definition proof-kompiled

# spec.k contains one positive target claim; run the complete SPEC module.
kprove spec.k \
  --definition proof-kompiled \
  --spec-module SPEC | tee positive-proof-output.txt
grep -qx '#Top' positive-proof-output.txt
