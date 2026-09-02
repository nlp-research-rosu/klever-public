#!/usr/bin/env bash
set -euo pipefail
cd /tmp/audit-work/12-longest-audit

export PATH="/home/agent/.nix-profile/bin:$PATH"

echo '$ kompile --version'
kompile --version
echo '$ kprove --version'
kprove --version
echo '$ krun --version'
krun --version

echo '$ kompile semantic.k --backend llvm --enable-search --main-module MPY-SEMANTICS --syntax-module MPY-SYNTAX --output-definition semantic-concrete-search-kompiled'
kompile semantic.k \
  --backend llvm \
  --enable-search \
  --main-module MPY-SEMANTICS \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-concrete-search-kompiled

echo '$ kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-fresh-kompiled'
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-fresh-kompiled

echo '$ python3 /audit-output/evidence/k_concrete_compare.py'
python3 /audit-output/evidence/k_concrete_compare.py

echo 'SCRIPT_EXIT_STATUS=0'
