#!/usr/bin/env bash
set -euo pipefail
set -x

cd /tmp/audit-work/fresh
test ! -e semantic-kompiled
kompile semantic.k \
  --backend llvm \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-kompiled
python3 /audit-output/evidence/03-concrete-compare.py
