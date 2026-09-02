#!/usr/bin/env bash
set -euo pipefail

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition scan-nototal-kompiled
