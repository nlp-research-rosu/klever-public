#!/usr/bin/env bash
set -u

source_dir=/tmp/audit-work/source
definition=/tmp/audit-work/build/verification-kompiled
spec=audit-positive-claims.k
status=0

for claim_number in 1 2 3 4 5 6 7 8 9; do
  module="AUDIT-CLAIM-${claim_number}"
  log="/audit-output/evidence/stage3-kprove-claim-${claim_number}.log"
  if ! /audit-output/evidence/run_logged.sh "$log" \
      kprove "$spec" --definition "$definition" --spec-module "$module"; then
    status=1
  elif ! rg -q '^#Top$' "$log"; then
    printf 'MISSING #Top for %s\n' "$module"
    status=1
  fi
done

exit "$status"
