#!/usr/bin/env bash
set -u

spec=/tmp/audit-work/38-decode-cyclic-audit/nonvacuity/spec-vacuity.k
proof=/tmp/audit-work/38-decode-cyclic-audit/build-proof/verification-kompiled
dry=/audit-output/evidence/06-nonvacuity-dry-run.raw.log
raw=/audit-output/evidence/06-nonvacuity-proof.raw.log
overall=0

printf 'False mutation: append "!" to the result-constraining destination.\n'
printf 'Satisfying counterexample: S=""; actual="", mutated required result="!".\n'

printf '\n$ kprove %q --definition %q --spec-module SPEC-VACUITY --dry-run > %q 2>&1\n' \
  "$spec" "$proof" "$dry"
kprove "$spec" \
  --definition "$proof" \
  --spec-module SPEC-VACUITY \
  --dry-run > "$dry" 2>&1
dry_status=$?
printf '[exit %d]\n' "$dry_status"
printf '$ wc -c %q\n' "$dry"
wc -c "$dry"
printf '$ sha256sum %q\n' "$dry"
sha256sum "$dry"
printf '$ tail -n 20 %q\n' "$dry"
tail -n 20 "$dry"
if [ "$dry_status" -ne 0 ]; then
  printf '[mutation build/dry-run failed unexpectedly]\n'
  overall=1
fi

printf '\n$ kprove %q --definition %q --spec-module SPEC-VACUITY\n' \
  "$spec" "$proof"
kprove "$spec" \
  --definition "$proof" \
  --spec-module SPEC-VACUITY > "$raw" 2>&1
proof_status=$?
tail -n 120 "$raw"
printf '[exit %d]\n' "$proof_status"

if [ "$proof_status" -eq 0 ]; then
  printf '[unexpected closure: false mutation exited zero]\n'
  overall=1
elif ! rg -q 'WarnStuckClaimState|cannot be rewritten further|implication check' "$raw"; then
  printf '[unexpected failure mode: no unmet-obligation residual]\n'
  overall=1
elif rg -xq '#Top' "$raw"; then
  printf '[unexpected #Top in false mutation output]\n'
  overall=1
else
  printf '[expected meaningful proof failure observed]\n'
fi

printf '\nOverall non-vacuity test status: %d\n' "$overall"
exit "$overall"
