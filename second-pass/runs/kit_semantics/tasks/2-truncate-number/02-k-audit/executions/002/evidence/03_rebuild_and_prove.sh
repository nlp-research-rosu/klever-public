#!/usr/bin/env bash
set -euo pipefail
set -x

scratch=/tmp/audit-work/fresh
cd "$scratch"

command -v kompile
command -v krun
command -v kprove
kompile --version
krun --version
kprove --version

test ! -e audit-runtime-kompiled
test ! -e audit-verification-kompiled

python3 py2mpy.py audit-smoke.py > audit-smoke.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled

krun regenerated-solution.mpy \
  --definition audit-runtime-kompiled

krun audit-smoke.mpy \
  --definition audit-runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled

kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC

