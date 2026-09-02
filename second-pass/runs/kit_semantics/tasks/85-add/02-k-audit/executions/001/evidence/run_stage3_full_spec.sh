#!/usr/bin/env bash
set -u

export PATH="$HOME/.nix-profile/bin:$PATH"
cd /tmp/audit-work/fresh

printf '%s\n' \
  'COMMAND: kprove spec.k --definition audit-verification-kompiled --spec-module SPEC'
kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC
status=$?
printf 'EXIT: %s\n' "$status"
exit "$status"
