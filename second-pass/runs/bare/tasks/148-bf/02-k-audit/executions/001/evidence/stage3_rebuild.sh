#!/usr/bin/env bash
set -euo pipefail
set -x

command -v kompile
command -v krun
command -v kprove
kompile --version
krun --version
kprove --version

python3 /reference/py2mpy.py solution.py > solution-audit-regenerated.mpy
cmp solution.mpy solution-audit-regenerated.mpy

sha256sum solution-program.k spec.k mutation-spec.k
python3 generate_proof_artifacts.py
cmp solution-program.k /tmp/audit-work/candidate-src/solution-program.k
cmp spec.k /tmp/audit-work/candidate-src/spec.k
cmp mutation-spec.k /tmp/audit-work/candidate-src/mutation-spec.k
sha256sum solution-program.k spec.k mutation-spec.k

kompile semantic.k \
  --backend llvm \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-audit-kompiled

python3 /audit-output/evidence/concrete_compare.py

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition verification-audit-kompiled

test "$(rg -c '^  claim$' spec.k)" -eq 73
rg -c '^  claim$' spec.k

kprove spec.k \
  --definition verification-audit-kompiled \
  --spec-module BF-SPEC
