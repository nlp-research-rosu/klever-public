#!/usr/bin/env sh
exec kast \
  --definition /reference/k-proof/verification-kompiled \
  --module VERIFICATION \
  --sort Module \
  --output kore "$@"
