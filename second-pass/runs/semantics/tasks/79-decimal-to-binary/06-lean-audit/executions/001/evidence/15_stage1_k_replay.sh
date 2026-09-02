#!/usr/bin/env bash
set -euo pipefail

audit_stage1_dir=/tmp/audit-work/stage1-replay
if [[ -e "$audit_stage1_dir" ]]; then
  echo "refusing to reuse non-fresh path: $audit_stage1_dir" >&2
  exit 97
fi

echo '$ mkdir -p /tmp/audit-work/stage1-replay'
mkdir -p "$audit_stage1_dir"

echo '$ cp -a /reference/k-proof/. /tmp/audit-work/stage1-replay/'
cp -a /reference/k-proof/. "$audit_stage1_dir/"
cd "$audit_stage1_dir"

echo '$ kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled'
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

echo '$ kprove spec.k --definition verification-kompiled --spec-module SPEC --output pretty'
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --output pretty
