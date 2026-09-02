#!/usr/bin/env bash
set -uo pipefail

scratch_path=$(sed -n '1p' /audit-output/evidence/scratch-path.txt)
log_path=/audit-output/evidence/05_static_review.log
inventory_path=/audit-output/evidence/05_rule_inventory.md
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

printf 'Exhaustive static review support (UTC): '
date -u +%Y-%m-%dT%H:%M:%SZ

run python3 /audit-output/evidence/05_inventory.py "$scratch_path" "$inventory_path"
run wc -l -c "$inventory_path"
run sed -n 1,80p "$inventory_path"
run tail -n 40 "$inventory_path"

run rg -n 'starts_one_ends|starts-one-ends|18 \\*Int|Int\\(18\\)' \
    "$scratch_path/reference-semantics"
run rg -n '^  (syntax|rule|context|configuration|claim)\\b' \
    "$scratch_path/verification.k"
run rg -n '\[(simplification|simp)\b|\bfunctional\b' \
    "$scratch_path/reference-semantics" \
    "$scratch_path/verification.k"
run rg -n 'no-evaluators|\[function|\btotal\b|\[priority\(' \
    "$scratch_path/reference-semantics"

run sed -n 1,120p "$scratch_path/reference-semantics/semantics.k"
run sed -n 1,120p "$scratch_path/verification.k"
run sed -n 1,140p "$scratch_path/solution.mpy"

printf '\nScript exit: 0 (individual command statuses above; exit 1 from negative rg means no matches)\n'
