#!/usr/bin/env bash
set -u
set -o pipefail

exec > >(tee /audit-output/evidence/stage4-constructor-kore-compare.log) 2>&1
set -x

cd /tmp/audit-work/reconstruction || exit 90

python3 /audit-output/evidence/constructor_compare.py
surface_status=$?
printf 'surface_constructor_compare_exit=%d\n' "$surface_status"

kast source-body-term.mpy \
  --definition verification-audit-kompiled \
  --module VERIFICATION \
  --sort Stmt \
  --output kore > source-body-term.kore
source_kast_status=$?
printf 'source_body_kast_exit=%d\n' "$source_kast_status"

kast claim-body-term.mpy \
  --definition verification-audit-kompiled \
  --module VERIFICATION \
  --sort Stmt \
  --output kore > claim-body-term.kore
claim_kast_status=$?
printf 'claim_body_kast_exit=%d\n' "$claim_kast_status"

cmp -s source-body-term.kore claim-body-term.kore
kore_identity_status=$?
printf 'parsed_body_constructor_kore_identity_exit=%d\n' "$kore_identity_status"

sha256sum source-body-term.kore claim-body-term.kore
hash_status=$?
printf 'parsed_body_hash_exit=%d\n' "$hash_status"

if [[ "$surface_status" -ne 0 ]] ||
   [[ "$source_kast_status" -ne 0 ]] ||
   [[ "$claim_kast_status" -ne 0 ]] ||
   [[ "$kore_identity_status" -ne 0 ]] ||
   [[ "$hash_status" -ne 0 ]]; then
  exit 1
fi
