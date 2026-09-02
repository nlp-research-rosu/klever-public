#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/77-iscube
src="$scratch/candidate-src"
definition="$scratch/audit-cube-verification-kompiled"
mutation="$src/spec-vacuity-review.k"
dry_stdout="$scratch/vacuity-dry-run.stdout"
dry_stderr="$scratch/vacuity-dry-run.stderr"

printf '%s\n' 'Satisfying original precondition witness: N=1, input=cube(1)=1.'
printf '%s\n' 'Original claim requires BoolVal(true); mutation requires BoolVal(false).'
printf '%s\n' '$ nl -ba spec-vacuity-review.k'
nl -ba "$mutation"
printf '[exit %d]\n' "$?"

printf '\n$ kprove %q --definition %q --spec-module AUDIT-VACUITY-SPEC --dry-run > %q 2> %q\n' \
  "$mutation" "$definition" "$dry_stdout" "$dry_stderr"
kprove "$mutation" \
  --definition "$definition" \
  --spec-module AUDIT-VACUITY-SPEC \
  --dry-run >"$dry_stdout" 2>"$dry_stderr"
dry_status=$?
printf '[exit %d]\n' "$dry_status"
wc -c "$dry_stdout" "$dry_stderr"
sha256sum "$dry_stdout" "$dry_stderr"
if [[ -s "$dry_stderr" ]]; then
  sed -n '1,80p' "$dry_stderr"
fi

printf '\n$ kprove %q --definition %q --spec-module AUDIT-VACUITY-SPEC\n' \
  "$mutation" "$definition"
proof_output="$(
  kprove "$mutation" \
    --definition "$definition" \
    --spec-module AUDIT-VACUITY-SPEC 2>&1
)"
proof_status=$?
printf '%s\n' "$proof_output"
printf '[exit %d; nonzero is expected]\n' "$proof_status"

if (( dry_status == 0 && proof_status != 0 )) \
  && grep -q 'WarnStuckClaimState' <<<"$proof_output" \
  && grep -q 'BoolVal ( true )' <<<"$proof_output" \
  && grep -q "doesn't unify with the destination" <<<"$proof_output"; then
  printf '%s\n' 'NONVACUITY=PASS'
  exit 0
fi

printf '%s\n' 'NONVACUITY=FAIL'
exit 1
