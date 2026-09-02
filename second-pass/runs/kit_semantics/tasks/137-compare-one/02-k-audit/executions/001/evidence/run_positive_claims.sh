#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence
claims=(
  int-int
  int-float
  float-int
  float-float
  int-str
  str-int
  float-str
  str-float
  str-str
)

overall=0
for claim in "${claims[@]}"; do
  log="$evidence/positive-${claim}.log"
  command=(kprove spec.k --definition verification-kompiled --spec-module SPEC --claims "SPEC.${claim}")
  printf 'COMMAND:' | tee "$log"
  printf ' %q' "${command[@]}" | tee -a "$log"
  printf '\n' | tee -a "$log"
  (
    cd "$work" || exit 125
    "${command[@]}"
  ) 2>&1 | tee -a "$log"
  status=${PIPESTATUS[0]}
  printf 'EXIT_STATUS: %s\n' "$status" | tee -a "$log"
  top_count=$(grep -c '^#Top$' "$log" || true)
  printf 'TOP_COUNT: %s\n' "$top_count" | tee -a "$log"
  if [[ $status -ne 0 || $top_count -ne 1 ]]; then
    overall=1
  fi
done
printf 'OVERALL_EXIT_STATUS: %s\n' "$overall" | tee "$evidence/positive-claims-summary.log"
exit "$overall"
