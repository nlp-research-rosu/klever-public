#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence
runner=$evidence/run_logged.sh
labels=(
  audit-entry-example
  audit-entry-half
  audit-entry-quarter
  audit-loop-whole
  audit-loop-half
  audit-loop-quarter
  audit-loop-base
  audit-bridge-whole
  audit-bridge-half
  audit-bridge-quarter
)

failures=0
cd "$work" || exit 1
for label in "${labels[@]}"; do
  if ! "$runner" "$evidence/12-proof-$label.log" \
      kprove spec-labelled.k \
      --definition fresh-verification-kompiled \
      --spec-module SPEC-AUDIT \
      --claims "SPEC-AUDIT.$label"; then
    failures=$((failures + 1))
  fi
done

printf 'claims_run=%d failures=%d\n' "${#labels[@]}" "$failures"
exit "$failures"
