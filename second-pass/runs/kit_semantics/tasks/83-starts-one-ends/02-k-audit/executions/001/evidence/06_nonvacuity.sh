#!/usr/bin/env bash
set -uo pipefail

scratch_path=$(sed -n '1p' /audit-output/evidence/scratch-path.txt)
log_path=/audit-output/evidence/06_nonvacuity.log
exec >"$log_path" 2>&1

run_bounded() {
    local label=$1
    shift
    local raw_path="$scratch_path/reviewer-${label}.raw.log"
    printf '\n$'
    printf ' %q' "$@"
    printf '\n'
    "$@" >"$raw_path" 2>&1
    last_status=$?
    printf '[exit %d]\n' "$last_status"
    printf '[raw output: %s; ' "$raw_path"
    wc -c <"$raw_path" | tr -d '\n'
    printf ' bytes; '
    wc -l <"$raw_path" | tr -d '\n'
    printf ' lines]\n'
    sed -n '1,180p' "$raw_path"
    line_count=$(wc -l <"$raw_path")
    if [ "$line_count" -gt 360 ]; then
        printf '[... middle omitted from bounded evidence ...]\n'
        tail -n 180 "$raw_path"
    elif [ "$line_count" -gt 180 ]; then
        sed -n '181,360p' "$raw_path"
    fi
}

printf 'Fresh non-vacuity test (UTC): '
date -u +%Y-%m-%dT%H:%M:%SZ
printf 'Scratch: %s\n' "$scratch_path"

printf '\n$ cp -a /audit-output/evidence/06_reviewer_false_result.k %q/reviewer-false-result.k\n' "$scratch_path"
cp -a /audit-output/evidence/06_reviewer_false_result.k "$scratch_path/reviewer-false-result.k"
printf '[exit %d]\n' "$?"

run_bounded mutation-witness \
    python3 /audit-output/evidence/06_mutation_witness.py \
    "$scratch_path/trusted-canonical.py" \
    "$scratch_path/solution.py"
witness_status=$last_status

printf '\n$ cd %q\n' "$scratch_path"
cd "$scratch_path" || exit 2
printf '[exit 0]\n'

run_bounded false-dry-run \
    kprove reviewer-false-result.k \
    --definition reviewer-verification-kompiled \
    --spec-module REVIEWER-FALSE-RESULT \
    --dry-run
dry_status=$last_status

run_bounded false-proof \
    kprove reviewer-false-result.k \
    --definition reviewer-verification-kompiled \
    --spec-module REVIEWER-FALSE-RESULT
proof_status=$last_status

printf '\nExpected-signal checks:\n'
printf 'witness_exit_zero = %s\n' "$([ "$witness_status" -eq 0 ] && printf true || printf false)"
printf 'dry_run_exit_zero = %s\n' "$([ "$dry_status" -eq 0 ] && printf true || printf false)"
printf 'proof_exit_nonzero = %s\n' "$([ "$proof_status" -ne 0 ] && printf true || printf false)"
false_log="$scratch_path/reviewer-false-proof.raw.log"
printf 'has_WarnStuckClaimState = %s\n' "$(grep -q 'WarnStuckClaimState' "$false_log" && printf true || printf false)"
printf 'has_implication_failure = %s\n' "$(grep -q 'implication check between the conditions has failed' "$false_log" && printf true || printf false)"
printf 'mentions_actual_180 = %s\n' "$(grep -q '180' "$false_log" && printf true || printf false)"
printf 'mentions_false_181 = %s\n' "$(grep -q '181' "$false_log" && printf true || printf false)"

printf '\nScript exit: 0 (the false proof is expected to exit nonzero)\n'
