#!/usr/bin/env bash
set -euo pipefail
set -x

kompile --version
krun --version
kompile \
  --backend llvm \
  /tmp/audit-work/candidate-src/semantic.k \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/semantic-fresh-kompiled
