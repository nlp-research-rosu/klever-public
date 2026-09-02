#!/usr/bin/env bash
set -euo pipefail

kompile semantic.k \
  --backend llvm \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-semantic-kompiled
