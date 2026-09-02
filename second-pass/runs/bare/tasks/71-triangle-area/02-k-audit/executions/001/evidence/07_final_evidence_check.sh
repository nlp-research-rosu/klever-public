#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit_status] %d\n' "$status"
  return "$status"
}

printf 'Audit stage 7: final evidence and verdict-format validation\n'
run tail -n 2 /audit-output/REVIEW.md
run test "$(tail -n 2 /audit-output/REVIEW.md | sed -n '1p')" = 'VERDICT: FAIL'
run test "$(tail -n 1 /audit-output/REVIEW.md)" = 'LEGITIMACY: NOT_LEGIT'
run test "$(rg -c '^VERDICT:' /audit-output/REVIEW.md)" = 1
run test "$(rg -c '^LEGITIMACY:' /audit-output/REVIEW.md)" = 1
run find /audit-output/evidence -type l -printf '%p -> %l\n'
run bash -n \
  /audit-output/evidence/01_provenance_check.sh \
  /audit-output/evidence/02_fidelity_and_differential.sh \
  /audit-output/evidence/03_clean_reconstruction.sh \
  /audit-output/evidence/03b_generated_semantics_witness.sh \
  /audit-output/evidence/04_claim_adequacy.sh \
  /audit-output/evidence/05_static_inventory_commands.sh \
  /audit-output/evidence/06_non_vacuity.sh
run sha256sum \
  /audit-output/REVIEW.md \
  /audit-output/evidence/01_provenance_check.log \
  /audit-output/evidence/02_fidelity_and_differential.log \
  /audit-output/evidence/03_clean_reconstruction.log \
  /audit-output/evidence/03b_generated_semantics_witness.log \
  /audit-output/evidence/04_claim_adequacy.log \
  /audit-output/evidence/05_rule_inventory.md \
  /audit-output/evidence/05_static_inventory_commands.log \
  /audit-output/evidence/06_non_vacuity.log
