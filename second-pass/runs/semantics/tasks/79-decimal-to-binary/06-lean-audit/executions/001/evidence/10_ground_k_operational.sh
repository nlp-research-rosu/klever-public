#!/usr/bin/env bash
set -euo pipefail

audit_k_dir=/tmp/audit-work/k-operational

echo '$ cp -a /reference/k-proof/reference-semantics /tmp/audit-work/k-operational/reference-semantics'
cp -a /reference/k-proof/reference-semantics "$audit_k_dir/reference-semantics"

echo '$ kompile operational-audit.k --backend haskell --main-module OPERATIONAL-AUDIT --syntax-module MPY-SYNTAX --output-definition operational-kompiled'
cd "$audit_k_dir"
kompile operational-audit.k \
  --backend haskell \
  --main-module OPERATIONAL-AUDIT \
  --syntax-module MPY-SYNTAX \
  --output-definition operational-kompiled

echo '$ kprove operational-spec.k --definition operational-kompiled --spec-module OPERATIONAL-SPEC --output pretty'
kprove operational-spec.k \
  --definition operational-kompiled \
  --spec-module OPERATIONAL-SPEC \
  --output pretty
