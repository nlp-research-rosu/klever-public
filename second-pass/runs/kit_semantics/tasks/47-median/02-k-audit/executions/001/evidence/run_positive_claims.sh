#!/usr/bin/env bash
set -u

work=/tmp/audit-work/47-median/candidate-src
definition=/tmp/audit-work/47-median/fresh-verification-kompiled
evidence=/audit-output/evidence
claims=(
  median-odd
  median-even-int-int
  median-even-int-bool
  median-even-bool-int
  median-even-bool-bool
  median-even-float-float
  median-even-int-float
  median-even-float-int
  median-even-bool-float
  median-even-float-bool
)

overall=0
cd "$work" || exit 125
: > "$evidence/03-positive-claims-summary.log"
for label in "${claims[@]}"; do
  log="$evidence/03-kprove-$label.log"
  command_text="kprove spec.k --definition $definition --spec-module SPEC --claims SPEC.$label"
  printf 'COMMAND=%s\n' "$command_text" > "$log"
  kprove spec.k \
    --definition "$definition" \
    --spec-module SPEC \
    --claims "SPEC.$label" >> "$log" 2>&1
  status=$?
  printf 'EXIT_STATUS=%s\n' "$status" >> "$log"
  tops=$(grep -c '^#Top$' "$log" || true)
  printf '%s exit=%s top_lines=%s log=%s\n' \
    "$label" "$status" "$tops" "$log" |
    tee -a "$evidence/03-positive-claims-summary.log"
  if [[ "$status" -ne 0 || "$tops" -ne 1 ]]; then
    overall=1
  fi
done
printf 'OVERALL_EXIT_STATUS=%s\n' "$overall" |
  tee -a "$evidence/03-positive-claims-summary.log"
exit "$overall"
