#!/usr/bin/env bash
set -euxo pipefail

kompile --version
kprove --version
krun --version

test ! -e /tmp/audit-work/fresh/concrete-kompiled
test ! -e /tmp/audit-work/fresh/proof-kompiled

kompile /tmp/audit-work/fresh/semantic.k \
  --backend llvm \
  --main-module MPY-SEMANTICS \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/fresh/concrete-kompiled

kompile /tmp/audit-work/fresh/semantic.k \
  --backend haskell \
  --main-module MPY-SEMANTICS \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/fresh/proof-kompiled

sha256sum \
  /tmp/audit-work/fresh/semantic.k \
  /tmp/audit-work/fresh/verification.k \
  /tmp/audit-work/fresh/spec.k \
  /tmp/audit-work/fresh/concrete-kompiled/definition.kore \
  /tmp/audit-work/fresh/proof-kompiled/definition.kore
sed -n '1,20p' /tmp/audit-work/fresh/concrete-kompiled/backend.txt
sed -n '1,20p' /tmp/audit-work/fresh/proof-kompiled/backend.txt
