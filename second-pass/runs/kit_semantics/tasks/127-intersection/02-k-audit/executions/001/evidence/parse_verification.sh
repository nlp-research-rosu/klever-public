#!/usr/bin/env bash
exec kast \
  --definition /tmp/audit-work/127-intersection/verification-kompiled \
  --module VERIFICATION \
  --output kore \
  "$@"
