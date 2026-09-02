#!/usr/bin/env bash
set -u
set -o pipefail

cd /tmp/audit-work/125-split-words
cp /audit-output/evidence/05_bridge_false_witnesses.k bridge-false-witnesses.k
cp /audit-output/evidence/05_fixed_false_witnesses.k fixed-false-witnesses.k

echo '$ kprove bridge-false-witnesses.k --definition audit-verification-kompiled --spec-module BRIDGE-FALSE-WITNESSES'
kprove bridge-false-witnesses.k \
  --definition audit-verification-kompiled \
  --spec-module BRIDGE-FALSE-WITNESSES
echo "extended_false_witnesses_exit=$?"

echo '$ kompile reference-semantics/semantics.k --backend haskell --main-module MPY --syntax-module MPY-SYNTAX --output-definition audit-fixed-kompiled'
kompile reference-semantics/semantics.k \
  --backend haskell \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-fixed-kompiled
echo "fixed_haskell_kompile_exit=$?"

echo '$ kprove fixed-false-witnesses.k --definition audit-fixed-kompiled --spec-module FIXED-FALSE-WITNESSES'
kprove fixed-false-witnesses.k \
  --definition audit-fixed-kompiled \
  --spec-module FIXED-FALSE-WITNESSES
echo "fixed_false_witnesses_exit=$?"
