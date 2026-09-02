#!/usr/bin/env bash
set -u
cd /tmp/audit-work/source

claims=(
  ds0
  ds1
  ds11
  ds_neg1
  ds_neg11
  ds_neg12
  ds_neg123
  order_symbolic
)

overall=0
for claim_name in "${claims[@]}"; do
  log="/audit-output/evidence/kprove_${claim_name}.log"
  printf '%s\n' \
    "COMMAND: kprove spec-labeled.k --definition verification-kompiled --spec-module ORDER-BY-POINTS-SPEC-LABELED --claims ${claim_name}" \
    > "$log"
  kprove \
    spec-labeled.k \
    --definition verification-kompiled \
    --spec-module ORDER-BY-POINTS-SPEC-LABELED \
    --claims "$claim_name" \
    >> "$log" 2>&1
  status=$?
  printf 'EXIT_STATUS: %s\n' "$status" >> "$log"
  printf '%s claim=%s top_count=%s\n' \
    "RESULT:" \
    "$claim_name" \
    "$(rg -c '^#Top$' "$log" || true)"
  printf 'EXIT_STATUS: %s\n' "$status"
  if [[ "$status" -ne 0 ]] || ! rg -q '^#Top$' "$log"; then
    overall=1
  fi
done

printf 'OVERALL_EXIT_STATUS: %s\n' "$overall"
exit "$overall"
