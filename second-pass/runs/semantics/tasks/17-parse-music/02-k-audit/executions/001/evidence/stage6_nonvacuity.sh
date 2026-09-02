#!/usr/bin/env bash
set -u
set -o pipefail
set -x

work=/tmp/audit-work/reconstruction
cp /audit-output/evidence/spec-vacuity.k "$work/spec-vacuity.k"
cd "$work" || exit 90

python3 -c 'from solution import parse_music; result = parse_music(""); print("generated empty witness =", result); assert result == []'
generated_witness_status=$?
python3 -c 'import importlib.util; s=importlib.util.spec_from_file_location("canonical","/reference/canonical.py"); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); result=m.parse_music(""); print("canonical empty witness =",result); assert result == []'
canonical_witness_status=$?
printf 'satisfying witness exits: generated=%d canonical=%d\n' \
  "$generated_witness_status" "$canonical_witness_status"

kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module PARSE-MUSIC-ENTRY-VACUITY \
  --dry-run > /tmp/audit-work/vacuity-dry-run.kore
dry_run_status=$?
printf 'false mutation dry-run/build exit: %d\n' "$dry_run_status"
wc -c /tmp/audit-work/vacuity-dry-run.kore

kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module PARSE-MUSIC-ENTRY-VACUITY \
  --branching-allowed 100
mutation_proof_status=$?
printf 'false mutation kprove exit (nonzero expected): %d\n' "$mutation_proof_status"

if test "$generated_witness_status" -ne 0 \
  || test "$canonical_witness_status" -ne 0 \
  || test "$dry_run_status" -ne 0; then
  exit 1
fi
if test "$mutation_proof_status" -eq 0; then
  exit 2
fi
exit 0
