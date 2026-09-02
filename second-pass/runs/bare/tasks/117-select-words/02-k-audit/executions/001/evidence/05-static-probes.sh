#!/usr/bin/env bash
set -euo pipefail
set -x

cd /tmp/audit-work/fresh
diff -u semantic-no-eval.k semantic.k || true
if test ! -e semantic-no-eval-kompiled; then
  kompile semantic-no-eval.k \
    --backend llvm \
    --main-module SEMANTIC \
    --syntax-module MPY-SYNTAX \
    --output-definition semantic-no-eval-kompiled
fi
python3 /audit-output/evidence/05-static-probes.py
