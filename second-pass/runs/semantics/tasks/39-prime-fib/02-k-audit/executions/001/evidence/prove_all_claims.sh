#!/usr/bin/env bash
set -uo pipefail

overall=0
for index in $(seq 1 11); do
  label=$(printf '12_kprove_pf%02d' "$index")
  /audit-output/evidence/run_logged.sh \
    "$label" \
    /tmp/audit-work/work \
    kprove spec.k \
      --definition proof-kompiled \
      --spec-module PRIME-FIB-SPEC \
      --claims "PRIME-FIB-SPEC.pf${index}"
  status=$?
  printf 'CLAIM pf%d EXIT_STATUS=%d\n' "$index" "$status"
  if (( status != 0 )); then
    overall=1
  fi
done
exit "$overall"
