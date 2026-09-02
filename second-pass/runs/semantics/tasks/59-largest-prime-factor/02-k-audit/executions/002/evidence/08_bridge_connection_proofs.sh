#!/usr/bin/env bash
set -uo pipefail

SCRATCH=/tmp/audit-work/59-lpf
EVIDENCE=/audit-output/evidence
cd "$SCRATCH" || exit 1

echo "$ kompile fixed-verification.k --backend haskell --main-module FIXED-VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-fixed-verification-kompiled"
kompile fixed-verification.k \
  --backend haskell \
  --main-module FIXED-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-fixed-verification-kompiled \
  > "$EVIDENCE/08_fixed_verification_kompile.log" 2>&1
build_status=$?
echo "kompile_exit=$build_status"
if [ "$build_status" -ne 0 ]; then
  tail -160 "$EVIDENCE/08_fixed_verification_kompile.log"
  exit "$build_status"
fi

overall=0
for label in compare-gt compare-mod-zero assign-floor augassign-one return-factor; do
  log="$EVIDENCE/08_bridge_${label}.log"
  echo "$ kprove bridge-connections.k --definition audit-fixed-verification-kompiled --spec-module BRIDGE-CONNECTIONS --claims BRIDGE-CONNECTIONS.$label"
  kprove bridge-connections.k \
    --definition audit-fixed-verification-kompiled \
    --spec-module BRIDGE-CONNECTIONS \
    --claims "BRIDGE-CONNECTIONS.$label" \
    > "$log" 2>&1
  status=$?
  echo "$label kprove_exit=$status"
  tail -100 "$log"
  if [ "$status" -ne 0 ] || ! rg -q '^#Top$' "$log"; then
    overall=1
  fi
done

echo "all_connection_claims_closed=$((1 - overall))"
exit "$overall"
