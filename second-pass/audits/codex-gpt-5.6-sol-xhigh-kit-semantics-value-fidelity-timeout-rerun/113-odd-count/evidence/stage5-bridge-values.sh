#!/usr/bin/env bash
set -u

BUILD=/tmp/audit-work/build/verification-kompiled
EVIDENCE=/audit-output/evidence
status=0

printf '$ kprove %s --definition %s --spec-module BRIDGE-CORRECT\n' \
  "$EVIDENCE/bridge-correct.k" "$BUILD"
kprove "$EVIDENCE/bridge-correct.k" \
  --definition "$BUILD" \
  --spec-module BRIDGE-CORRECT \
  > "$EVIDENCE/stage5-bridge-correct.log" 2>&1
correct_rc=$?
printf '[exit %d]\n' "$correct_rc"
tail -100 "$EVIDENCE/stage5-bridge-correct.log"
if (( correct_rc != 0 )); then status=1; fi

for label in count-wrong int-string-wrong; do
  log="$EVIDENCE/stage5-bridge-opposite-$label.log"
  printf '$ kprove %s --definition %s --spec-module BRIDGE-OPPOSITE --claims BRIDGE-OPPOSITE.%s\n' \
    "$EVIDENCE/bridge-opposite.k" "$BUILD" "$label"
  kprove "$EVIDENCE/bridge-opposite.k" \
    --definition "$BUILD" \
    --spec-module BRIDGE-OPPOSITE \
    --claims "BRIDGE-OPPOSITE.$label" \
    > "$log" 2>&1
  opposite_rc=$?
  printf '[exit %d; expected nonzero]\n' "$opposite_rc"
  tail -140 "$log"
  if (( opposite_rc == 0 )); then
    status=1
  fi
  if ! rg -q 'WarnStuckClaimState' "$log"; then
    status=1
  fi
done

printf 'Final bridge_value_status=%d\n' "$status"
exit "$status"
