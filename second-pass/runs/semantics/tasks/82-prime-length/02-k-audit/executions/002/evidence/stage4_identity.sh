#!/usr/bin/env bash
set -uo pipefail
set -x

cd /tmp/audit-work/prime-length-audit
kprove body-identity.k \
  --definition audit-verification-kompiled \
  --spec-module BODY-IDENTITY \
  --claims BODY-IDENTITY.submitted-body
command_status=$?
echo "EXIT_STATUS=${command_status} COMMAND=kprove body-identity.k --definition audit-verification-kompiled --spec-module BODY-IDENTITY --claims BODY-IDENTITY.submitted-body"
exit "$command_status"
