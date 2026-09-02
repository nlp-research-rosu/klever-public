#!/usr/bin/env bash
set -uo pipefail

scratch_path=$(sed -n '1p' /audit-output/evidence/scratch-path.txt)
log_path=/audit-output/evidence/04_body_sensitivity.log
exec >"$log_path" 2>&1

printf '$ cp -a /audit-output/evidence/04_reviewer_body_mutation.k %q/reviewer-body-mutation.k\n' "$scratch_path"
cp -a /audit-output/evidence/04_reviewer_body_mutation.k "$scratch_path/reviewer-body-mutation.k"
printf '[exit %d]\n' "$?"

printf '\n$ cd %q\n' "$scratch_path"
cd "$scratch_path" || exit 2
printf '[exit 0]\n'

dry_log="$scratch_path/reviewer-body-mutation-dry.raw.log"
printf '\n$ kprove reviewer-body-mutation.k --definition reviewer-verification-kompiled --spec-module REVIEWER-BODY-MUTATION --dry-run\n'
kprove reviewer-body-mutation.k \
    --definition reviewer-verification-kompiled \
    --spec-module REVIEWER-BODY-MUTATION \
    --dry-run >"$dry_log" 2>&1
dry_status=$?
printf '[exit %d]\n' "$dry_status"
sed -n '1,120p' "$dry_log"

proof_log="$scratch_path/reviewer-body-mutation-proof.raw.log"
printf '\n$ kprove reviewer-body-mutation.k --definition reviewer-verification-kompiled --spec-module REVIEWER-BODY-MUTATION\n'
kprove reviewer-body-mutation.k \
    --definition reviewer-verification-kompiled \
    --spec-module REVIEWER-BODY-MUTATION >"$proof_log" 2>&1
proof_status=$?
printf '[exit %d]\n' "$proof_status"
sed -n '1,180p' "$proof_log"
line_count=$(wc -l <"$proof_log")
if [ "$line_count" -gt 360 ]; then
    printf '[... middle omitted from bounded evidence ...]\n'
    tail -n 180 "$proof_log"
elif [ "$line_count" -gt 180 ]; then
    sed -n '181,360p' "$proof_log"
fi

printf '\nExpected-signal checks:\n'
printf 'dry_run_exit_zero = %s\n' "$([ "$dry_status" -eq 0 ] && printf true || printf false)"
printf 'proof_exit_nonzero = %s\n' "$([ "$proof_status" -ne 0 ] && printf true || printf false)"
printf 'has_WarnStuckClaimState = %s\n' "$(grep -q 'WarnStuckClaimState' "$proof_log" && printf true || printf false)"
printf 'mentions_mutated_actual_190 = %s\n' "$(grep -q '190' "$proof_log" && printf true || printf false)"

printf '\nScript exit: 0 (the body-mutated proof is expected to exit nonzero)\n'
