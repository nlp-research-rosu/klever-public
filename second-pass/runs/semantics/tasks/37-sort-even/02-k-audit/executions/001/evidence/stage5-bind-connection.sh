#!/usr/bin/env bash
set -u

work=/tmp/audit-work/37-sort-even-audit/bridge-check
evidence=/audit-output/evidence
build_log=$evidence/stage5-bind-connection-build.log
proof_log=$evidence/stage5-bind-connection-proof.log

cd "$work" || exit 1
if test -e bind-connection-kompiled; then
  echo 'refusing to reuse existing bridge-free definition'
  exit 2
fi

(
  echo '$ kompile bind-connection.k --backend haskell --main-module BIND-CONNECTION --syntax-module MPY-SYNTAX --output-definition bind-connection-kompiled'
  kompile bind-connection.k \
    --backend haskell \
    --main-module BIND-CONNECTION \
    --syntax-module MPY-SYNTAX \
    --output-definition bind-connection-kompiled
  command_status=$?
  echo "exit=$command_status"
  exit "$command_status"
) > "$build_log" 2>&1
build_status=$?
echo "bridge_free_build_exit=$build_status"
if test "$build_status" -ne 0; then
  exit 1
fi

(
  echo '$ kprove bind-connection-spec.k --definition bind-connection-kompiled --spec-module BIND-CONNECTION-SPEC --output pretty'
  kprove bind-connection-spec.k \
    --definition bind-connection-kompiled \
    --spec-module BIND-CONNECTION-SPEC \
    --output pretty
  command_status=$?
  echo "exit=$command_status"
  exit "$command_status"
) > "$proof_log" 2>&1
proof_status=$?
echo "bridge_free_proof_exit=$proof_status"
exit "$proof_status"
