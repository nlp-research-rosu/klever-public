#!/usr/bin/env bash
set -u

work_dir=/tmp/audit-work/candidate
evidence_dir=/audit-output/evidence
recorder=$evidence_dir/record_cmd.sh
definition=verification-proof-kompiled
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

overall=0
for claim in "${claims[@]}"; do
  (
    cd "$work_dir" || exit 70
    "$recorder" "$evidence_dir/stage3-claim-$claim.log" \
      kprove spec.k \
      --definition "$definition" \
      --spec-module SPEC \
      --claims "SPEC.$claim" \
      --warnings none
  )
  status=$?
  printf 'CLAIM %s EXIT_STATUS %d\n' "$claim" "$status"
  if (( status != 0 )); then
    overall=1
  fi
done

printf 'TOTAL_CLAIMS %d\n' "${#claims[@]}"
printf 'OVERALL_EXIT_STATUS %d\n' "$overall"
exit "$overall"
