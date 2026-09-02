#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/reconstruction
definition="$work/audit-verification-kompiled"
overall=0

for label in setup loop-invariant end-to-end; do
  selector="SPEC-LABELED.$label"
  if [[ "$label" == end-to-end ]]; then
    # The entry theorem uses both auxiliary claims. Keep its declared
    # dependencies available while selecting the target.
    selector='SPEC-LABELED.setup,SPEC-LABELED.loop-invariant,SPEC-LABELED.end-to-end'
  fi
  echo "CLAIM=$label"
  echo "AVAILABLE_CLAIMS=$selector"
  echo "COMMAND: timeout 900 kprove spec-labeled.k --definition audit-verification-kompiled --spec-module SPEC-LABELED --claims $selector"
  (
    cd "$work" || exit 98
    timeout 900 kprove spec-labeled.k \
      --definition "$definition" \
      --spec-module SPEC-LABELED \
      --claims "$selector"
  )
  status=$?
  echo "EXIT_STATUS=$status"
  if (( status != 0 )); then
    overall=1
  fi
done

echo "OVERALL_EACH_CLAIM_STATUS=$overall"
exit "$overall"
