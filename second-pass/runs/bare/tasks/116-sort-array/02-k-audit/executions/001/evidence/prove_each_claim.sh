#!/usr/bin/env bash
set -uo pipefail

if [[ $# -ne 4 ]]; then
  echo "usage: prove_each_claim.sh SPEC.k SPEC_MODULE DEFINITION LOG_DIR" >&2
  exit 64
fi

spec_file=$1
spec_module=$2
definition=$3
log_dir=$4
runner=/audit-output/evidence/run_logged.sh

claims=(
  count-correct
  comparator-correct
  insert-empty
  insert-at-front
  sort-empty-symbolic
  sort-singleton-symbolic
  sort-pair-before
  sort-pair-after
  sort-triple-abc
  sort-triple-bac
  sort-triple-bca
  sort-triple-acb
  sort-triple-cab
  sort-triple-cba
  example-one
  example-three
  empty
  duplicates
  wide-popcounts
  negative-extension
  example-ordered
  example-permutation
)

mkdir -p "$log_dir"
failures=0
for claim in "${claims[@]}"; do
  echo "START_CLAIM: $spec_module.$claim"
  "$runner" "$log_dir/$claim.log" \
    kprove "$spec_file" \
      --definition "$definition" \
      --spec-module "$spec_module" \
      --claims "$spec_module.$claim" \
      --warnings none
  claim_status=$?
  top_count=$(grep -c '^#Top$' "$log_dir/$claim.log" || true)
  echo "END_CLAIM: $spec_module.$claim status=$claim_status top_count=$top_count"
  if [[ $claim_status -ne 0 || $top_count -lt 1 ]]; then
    failures=$((failures + 1))
  fi
done

echo "SUMMARY claims=${#claims[@]} failures=$failures"
exit "$failures"
