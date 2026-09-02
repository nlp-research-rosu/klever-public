#!/usr/bin/env bash
set -euo pipefail
exec kast \
  --definition /tmp/audit-work/verification-haskell-kompiled \
  --module MPY-VERIFICATION \
  --sort Program \
  --output kore \
  "$@"
