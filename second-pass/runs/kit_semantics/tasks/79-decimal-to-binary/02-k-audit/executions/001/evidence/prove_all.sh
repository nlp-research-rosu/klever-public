#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/79-audit/source || exit 1
echo '$ kprove spec.k --definition fresh-verification-kompiled --spec-module SPEC'
kprove spec.k \
  --definition fresh-verification-kompiled \
  --spec-module SPEC
status=$?
echo "KPROVE_EXIT_STATUS=$status"
exit "$status"
