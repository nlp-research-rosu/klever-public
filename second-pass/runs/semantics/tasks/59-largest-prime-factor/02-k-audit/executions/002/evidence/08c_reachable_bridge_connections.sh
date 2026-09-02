#!/usr/bin/env bash
set -uo pipefail

SCRATCH=/tmp/audit-work/59-lpf
EVIDENCE=/audit-output/evidence
cd "$SCRATCH" || exit 1

overall=0
for label in compare-gt compare-mod-zero assign-floor augassign-one return-factor; do
  log="$EVIDENCE/08c_reachable_${label}.log"
  echo "$ timeout --foreground 45s kprove bridge-connections-reachable.k --definition audit-fixed-verification-kompiled --spec-module BRIDGE-CONNECTIONS-REACHABLE --claims BRIDGE-CONNECTIONS-REACHABLE.$label"
  timeout --foreground 45s \
    kprove bridge-connections-reachable.k \
      --definition audit-fixed-verification-kompiled \
      --spec-module BRIDGE-CONNECTIONS-REACHABLE \
      --claims "BRIDGE-CONNECTIONS-REACHABLE.$label" \
    > "$log" 2>&1
  status=$?
  top_count=$(rg -c '^#Top$' "$log" || true)
  echo "$label kprove_exit=$status top_count=$top_count"
  tail -80 "$log"
  if [ "$status" -ne 0 ] || [ "$top_count" -ne 1 ]; then
    overall=1
  fi
done
echo "all_reachable_connection_claims_closed=$((1 - overall))"
exit "$overall"
