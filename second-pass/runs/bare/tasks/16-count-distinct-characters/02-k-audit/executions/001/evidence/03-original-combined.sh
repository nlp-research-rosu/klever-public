#!/usr/bin/env bash
set +e
cd /tmp/audit-work/build || exit 90

echo '$ kprove spec.k --definition verification-kompiled --spec-module SPEC'
kprove spec.k --definition verification-kompiled --spec-module SPEC
status=$?
echo "exit=$status"
exit "$status"
