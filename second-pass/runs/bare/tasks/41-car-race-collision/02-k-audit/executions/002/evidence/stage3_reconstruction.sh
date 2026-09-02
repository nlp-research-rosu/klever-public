#!/usr/bin/env bash
set -u

run() {
  echo "\$ $*"
  "$@"
  status=$?
  echo "[exit $status]"
  return "$status"
}

run kompile --version

run timeout 600s kompile semantic.k \
  --backend llvm \
  --main-module SEMANTIC \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition concrete-kompiled

run python3 /audit-output/evidence/concrete_compare.py

run timeout 600s kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition proof-kompiled

run timeout 600s kprove spec.k \
  --definition proof-kompiled \
  --spec-module SPEC
