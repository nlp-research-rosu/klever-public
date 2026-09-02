#!/usr/bin/env bash
set -u
set -o pipefail

cd /tmp/audit-work/125-split-words
cp /audit-output/evidence/10_spec_vacuity.k spec-vacuity.k

echo '$ python3 -c witness for the false mutation'
python3 -c 'from solution import split_words; print("witness_empty_result=", split_words(""), sep=""); assert split_words("") == 0'
echo "mutation_witness_exit=$?"

echo '$ kprove spec-vacuity.k --definition audit-verification-kompiled --spec-module SPEC-VACUITY --claims SPEC-VACUITY.odd-lowercase-count --dry-run'
kprove spec-vacuity.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY \
  --claims SPEC-VACUITY.odd-lowercase-count \
  --dry-run
echo "mutation_dry_run_exit=$?"

echo '$ kprove spec-vacuity.k --definition audit-verification-kompiled --spec-module SPEC-VACUITY --claims SPEC-VACUITY.odd-lowercase-count'
kprove spec-vacuity.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY \
  --claims SPEC-VACUITY.odd-lowercase-count
echo "mutation_kprove_exit=$?"
