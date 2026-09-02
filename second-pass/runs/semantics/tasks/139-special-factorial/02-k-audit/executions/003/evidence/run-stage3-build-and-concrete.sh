#!/usr/bin/env bash
set -euo pipefail
set -x

export PATH=/home/agent/.nix-profile/bin:$PATH
cd /tmp/audit-work/case

kompile --version
kprove --version
krun --version

python3 trusted-py2mpy.py \
  /audit-output/evidence/concrete_driver.py \
  > audit-concrete.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled

krun audit-concrete.mpy \
  --definition audit-runtime-kompiled \
  --output pretty

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
