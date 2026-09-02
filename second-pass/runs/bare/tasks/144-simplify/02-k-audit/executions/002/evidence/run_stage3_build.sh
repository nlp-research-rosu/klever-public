#!/usr/bin/env bash
set -euxo pipefail

cd /tmp/audit-work/reconstruction
kompile --version
kompile --backend haskell semantic.k \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-semantic-kompiled
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
