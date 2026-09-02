#!/usr/bin/env bash
set +e
set -x

cd /tmp/audit-work/source || exit 90

grep -RIn '^[[:space:]]*claim\\b' --include='*.k' .
printf 'claim inventory grep exit: %s\n' "$?"

kprove spec.k \
  --definition /tmp/audit-work/proof-kompiled \
  --spec-module BY-LENGTH-SPEC
proof_exit=$?
printf 'positive target proof exit: %s\n' "$proof_exit"
exit "$proof_exit"
