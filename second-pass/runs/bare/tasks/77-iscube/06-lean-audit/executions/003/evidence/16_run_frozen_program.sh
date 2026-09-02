#!/usr/bin/env bash
set -euo pipefail
set -x

kompile /reference/k-proof/semantic.k \
  --backend llvm \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/iscube-semantic-kompiled
for input in -9 -8 -2 0 1 2 8 9 64 180; do
  krun /reference/k-proof/solution.mpy \
    -cN="$input" \
    --definition /tmp/audit-work/iscube-semantic-kompiled \
    --output pretty
done
