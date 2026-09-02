#!/usr/bin/env bash
set -euo pipefail
set -x

kprove --version
kompile \
  --backend haskell \
  /tmp/audit-work/candidate-src/verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/verification-fresh-kompiled
