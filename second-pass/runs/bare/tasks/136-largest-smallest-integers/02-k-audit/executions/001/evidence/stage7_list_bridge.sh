#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/reconstruction
definition="$work/list-bridge-kompiled"

echo 'PURPOSE: bridge arbitrary IntSeq to ordinary pyList(ListItem(pyInt(...))) without changing the submitted program body'
echo 'COMMAND: timeout 900 kompile verification-list-bridge.k --backend haskell --main-module VERIFICATION-LIST-BRIDGE --syntax-module MPY-SYNTAX --output-definition list-bridge-kompiled'
(
  cd "$work" || exit 98
  timeout 900 kompile verification-list-bridge.k \
    --backend haskell \
    --main-module VERIFICATION-LIST-BRIDGE \
    --syntax-module MPY-SYNTAX \
    --output-definition "$definition"
)
build_status=$?
echo "BUILD_EXIT_STATUS=$build_status"
if (( build_status != 0 )); then
  exit 1
fi

echo 'COMMAND: timeout 900 kprove spec-list-bridge.k --definition list-bridge-kompiled --spec-module SPEC-LIST-BRIDGE'
(
  cd "$work" || exit 98
  timeout 900 kprove spec-list-bridge.k \
    --definition "$definition" \
    --spec-module SPEC-LIST-BRIDGE
)
prove_status=$?
echo "PROOF_EXIT_STATUS=$prove_status"
if (( prove_status != 0 )); then
  exit 1
fi

echo 'LIST_REPRESENTATION_BRIDGE=PASS'
exit 0
