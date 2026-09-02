#!/usr/bin/env bash
exec kast --definition verification-kompiled \
  --module VERIFICATION \
  --sort Module \
  --output kore "$@"
