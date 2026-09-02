#!/usr/bin/env bash
set -euo pipefail
set -x

cd /tmp/audit-work/fresh
test ! -e verification-kompiled
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
rg -n '^[[:space:]]*claim([[:space:]]|$)' spec.k
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
