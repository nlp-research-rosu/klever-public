#!/usr/bin/env bash
set -u

LOG=/audit-output/evidence/stage4-5-static.log
exec > >(tee "$LOG") 2>&1

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

cd /tmp/audit-work || exit 1
status=0
printf 'STAGE 4 ADEQUACY AND STAGE 5 STATIC INVENTORY EVIDENCE\n'
run python3 /audit-output/evidence/program_pinning.py || status=1
run python3 /audit-output/evidence/claim_witnesses.py || status=1

printf 'concrete execution of the exact chooseNumProgram constant\n'
printf '$ kast run-chooseNumProgram-12-15.mpy --definition proof-kompiled --module VERIFICATION --sort Program --output kore > run-chooseNumProgram-12-15.kore\n'
kast run-chooseNumProgram-12-15.mpy \
  --definition proof-kompiled \
  --module VERIFICATION \
  --sort Program \
  --output kore \
  > run-chooseNumProgram-12-15.kore
kast_status=$?
printf '[exit %d]\n' "$kast_status"
if (( kast_status != 0 )); then status=1; fi
run_capture_output=run-chooseNumProgram-12-15.out
printf '$ krun run-chooseNumProgram-12-15.kore --parser cat --definition proof-kompiled | tee %s\n' "$run_capture_output"
krun run-chooseNumProgram-12-15.kore \
  --parser cat \
  --definition proof-kompiled \
  | tee "$run_capture_output"
krun_status=${PIPESTATUS[0]}
printf '[exit %d]\n' "$krun_status"
if (( krun_status != 0 )); then status=1; fi
run diff -u run-normal_prompt_example.out "$run_capture_output" || status=1

printf 'local declarations, attributes, rules, and claims\n'
run rg -n '^[[:space:]]*(syntax|configuration|rule|claim|requires|module|imports)' \
  semantic.k verification.k spec.k || status=1
printf 'special proof-relevant attributes\n'
run rg -n '\[(function|total|functional|simplification|concrete|priority|priorities|owise)' \
  semantic.k verification.k spec.k || status=1
printf 'explicit absence counts\n'
for token in total functional simplification concrete priority priorities owise opaque; do
  count=$(rg -i -o "\\b${token}\\b" semantic.k verification.k spec.k | wc -l)
  printf '%s_count=%s\n' "$token" "$count"
done

printf 'stage4_5_status=%d\n' "$status"
exit "$status"
