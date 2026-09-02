#!/usr/bin/env bash
set -u

run() {
  echo "\$ $*"
  "$@"
  status=$?
  echo "EXIT: $status"
  return "$status"
}

cd /tmp/audit-work/fresh || exit 125
echo '$ kast solution.mpy --definition audit-verification-kompiled --module MPY-SYNTAX --input program --output json > solution-kast.json'
kast solution.mpy \
  --definition audit-verification-kompiled \
  --module MPY-SYNTAX \
  --input program \
  --output json > solution-kast.json
status=$?
echo "EXIT: $status"
echo '$ kprove spec.k --definition audit-verification-kompiled --spec-module SPEC --dry-run --emit-json-spec audit-spec.json --output none'
kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC \
  --dry-run \
  --emit-json-spec audit-spec.json \
  --output none
status=$?
echo "EXIT: $status"
run python3 /audit-output/evidence/pinning_check.py
run python3 /audit-output/evidence/claim_instances.py
