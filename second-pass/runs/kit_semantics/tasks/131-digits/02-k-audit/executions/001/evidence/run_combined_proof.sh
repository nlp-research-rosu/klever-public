#!/usr/bin/env bash
set -o pipefail

cd /tmp/audit-work/source || exit 90

echo '$ kprove spec.k --definition /tmp/audit-work/rebuilt-verification-kompiled --spec-module SPEC'
kprove spec.k \
  --definition /tmp/audit-work/rebuilt-verification-kompiled \
  --spec-module SPEC
status=$?
echo "EXIT_STATUS=$status"
exit "$status"
