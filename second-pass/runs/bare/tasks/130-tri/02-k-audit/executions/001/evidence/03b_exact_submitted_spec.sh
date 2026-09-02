#!/usr/bin/env bash
set -euo pipefail
trap 'status=$?; printf "[audit] exit_status=%s\n" "$status"' EXIT
set -x

kprove /tmp/audit-work/130-tri/candidate/spec.k \
  --definition /tmp/audit-work/130-tri/build/verification-kompiled \
  --spec-module TRI-SPEC
