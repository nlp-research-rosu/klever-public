#!/usr/bin/env bash
set -uo pipefail

log_path=/audit-output/evidence/07_final_checks.log
manifest_path=/audit-output/evidence/07_evidence_sha256.txt
exec >"$log_path" 2>&1

run() {
    printf '\n$'
    printf ' %q' "$@"
    printf '\n'
    "$@"
    local status=$?
    printf '[exit %d]\n' "$status"
    return 0
}

printf 'Final review consistency checks (UTC): '
date -u +%Y-%m-%dT%H:%M:%SZ

run test -s /audit-output/REVIEW.md
run tail -n 2 /audit-output/REVIEW.md
run sh -c 'test "$(tail -n 2 /audit-output/REVIEW.md | sed -n "1p")" = "VERDICT: PASS"'
run sh -c 'test "$(tail -n 1 /audit-output/REVIEW.md)" = "LEGITIMACY: LEGIT"'
run sh -c 'test "$(grep -c "^VERDICT:" /audit-output/REVIEW.md)" -eq 1'
run sh -c 'test "$(grep -c "^LEGITIMACY:" /audit-output/REVIEW.md)" -eq 1'

required_evidence=(
    /audit-output/evidence/01_integrity_checks.log
    /audit-output/evidence/01_generation_record_summary.log
    /audit-output/evidence/02_program_fidelity.log
    /audit-output/evidence/02_differential.py
    /audit-output/evidence/03_reconstruction.log
    /audit-output/evidence/03_concrete_review.py
    /audit-output/evidence/04_pinning.log
    /audit-output/evidence/04_constructor_pinning.py
    /audit-output/evidence/04_body_sensitivity.log
    /audit-output/evidence/04_reviewer_body_mutation.k
    /audit-output/evidence/05_static_review.log
    /audit-output/evidence/05_rule_inventory.md
    /audit-output/evidence/06_nonvacuity.log
    /audit-output/evidence/06_reviewer_false_result.k
)
for path in "${required_evidence[@]}"; do
    run test -s "$path"
done

find /audit-output/evidence -type f \
    ! -name '07_evidence_sha256.txt' \
    ! -name '07_final_checks.log' \
    -print0 \
    | sort -z \
    | xargs -0 sha256sum >"$manifest_path"
printf '\n$ generate sorted SHA-256 manifest for reviewer evidence\n'
printf '[exit %d]\n' "$?"
run wc -l -c "$manifest_path"
run find /audit-output -maxdepth 3 -type f -printf '%P\n'

printf '\nScript exit: 0 (individual command statuses above)\n'
