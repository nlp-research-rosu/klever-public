#!/usr/bin/env bash
exec kast \
  --definition /tmp/audit-work/reconstruction/verification-kompiled \
  --module VERIFICATION \
  --sort Module \
  --output kore \
  "$@"
