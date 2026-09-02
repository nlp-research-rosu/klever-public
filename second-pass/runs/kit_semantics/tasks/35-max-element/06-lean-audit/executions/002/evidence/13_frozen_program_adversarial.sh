#!/usr/bin/env bash
set -euo pipefail
set -x

krun /audit-output/evidence/nan-smoke.mpy \
  --definition /reference/k-proof/runtime-kompiled
