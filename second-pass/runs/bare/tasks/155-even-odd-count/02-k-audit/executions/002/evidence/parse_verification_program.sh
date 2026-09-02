#!/usr/bin/env bash
set -euo pipefail
exec kast "$@" \
  --definition /tmp/audit-work/155-even-odd-count-audit/reconstruction/proof-fresh-kompiled \
  --module VERIFICATION \
  --output kore
