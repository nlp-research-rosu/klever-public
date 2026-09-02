#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence
overall=0

mkdir -p "$evidence/claim-specs"
for source in \
  spec-claim-integers.k \
  spec-claim-x-nonint.k \
  spec-claim-y-nonint.k \
  spec-claim-z-nonint.k
do
  cp "$work/$source" "$evidence/claim-specs/$source"
done

run_claim() {
  spec_file=$1
  spec_module=$2
  echo "\$ kprove $spec_file --definition verification-kompiled --spec-module $spec_module"
  (
    cd "$work" &&
    kprove "$spec_file" \
      --definition verification-kompiled \
      --spec-module "$spec_module"
  )
  status=$?
  echo "exit=$status"
  if test "$status" -ne 0; then
    overall=1
  fi
}

run_claim spec-claim-integers.k SPEC-CLAIM-INTEGERS
run_claim spec-claim-x-nonint.k SPEC-CLAIM-X-NONINT
run_claim spec-claim-y-nonint.k SPEC-CLAIM-Y-NONINT
run_claim spec-claim-z-nonint.k SPEC-CLAIM-Z-NONINT

exit "$overall"
