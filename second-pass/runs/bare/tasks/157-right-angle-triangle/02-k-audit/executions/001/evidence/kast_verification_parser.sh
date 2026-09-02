#!/usr/bin/env bash
set -euo pipefail

exec kast \
  --definition /tmp/audit-work/build/verification-kompiled \
  --module VERIFICATION \
  --sort Input \
  --output kore \
  "$@"
