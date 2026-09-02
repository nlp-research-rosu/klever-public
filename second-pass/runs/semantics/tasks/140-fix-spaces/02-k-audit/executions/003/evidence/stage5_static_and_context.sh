#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/140-fix-spaces/source
cd "$scratch" || exit 90
failures=0

run_proof() {
  local definition=$1
  local module=$2
  echo "$ kprove bridge-context-spec.k --definition $definition --spec-module $module"
  kprove bridge-context-spec.k \
    --definition "$definition" \
    --spec-module "$module"
  local status=$?
  echo "exit=$status"
  if [ "$status" -ne 0 ]; then
    failures=$((failures + 1))
  fi
}

echo '$ generate the exhaustive source declaration and rule inventory'
python3 /audit-output/evidence/static_inventory.py
inventory_status=$?
echo "exit=$inventory_status"
if [ "$inventory_status" -ne 0 ]; then
  failures=$((failures + 1))
fi

echo '$ fixed-semantics observable-continuation witnesses'
run_proof fresh-proof-base-kompiled TAIL-CONTEXT-SPEC
run_proof fresh-proof-base-kompiled STEP-CONTEXT-SPEC
run_proof fresh-proof-base-kompiled LOOP-CONTEXT-SPEC

echo '$ bridge-enabled observable-continuation witnesses'
run_proof fresh-proof-main-kompiled TAIL-CONTEXT-SPEC
run_proof fresh-proof-main-kompiled STEP-CONTEXT-SPEC
run_proof fresh-proof-main-kompiled LOOP-CONTEXT-SPEC

echo "audit_check_failures=$failures"
exit "$failures"
