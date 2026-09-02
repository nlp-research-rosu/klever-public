#!/usr/bin/env bash
set -u
set -o pipefail

exec > >(tee /audit-output/evidence/stage2_fidelity.log) 2>&1
set -x

cd /tmp/audit-work/reconstruction || exit 90

python3 py2mpy.py solution.py > regenerated-solution.mpy
translation_status=$?
printf 'trusted_translation_exit=%d\n' "$translation_status"

cmp -s regenerated-solution.mpy solution.mpy
identity_status=$?
printf 'submitted_solution_mpy_byte_identity_exit=%d\n' "$identity_status"

sha256sum solution.py solution.mpy regenerated-solution.mpy
hash_status=$?
printf 'solution_hash_exit=%d\n' "$hash_status"

python3 /audit-output/evidence/differential_test.py \
  > /audit-output/evidence/differential-results.jsonl
differential_status=$?
printf 'differential_test_exit=%d\n' "$differential_status"

tail -n 1 /audit-output/evidence/differential-results.jsonl
tail_status=$?
printf 'differential_summary_read_exit=%d\n' "$tail_status"

if [[ "$translation_status" -ne 0 ]] ||
   [[ "$identity_status" -ne 0 ]] ||
   [[ "$differential_status" -ne 0 ]]; then
  exit 1
fi
