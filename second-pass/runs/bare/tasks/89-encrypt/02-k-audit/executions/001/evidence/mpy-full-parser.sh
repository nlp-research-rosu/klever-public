#!/usr/bin/env bash
exec kast \
  --definition /tmp/audit-work/build/proof-kompiled \
  --module MPY \
  --sort Pgm \
  --output kore \
  "$@"
