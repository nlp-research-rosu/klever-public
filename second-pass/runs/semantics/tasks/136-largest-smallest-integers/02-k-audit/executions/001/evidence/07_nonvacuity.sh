#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/reconstruction
definition="$scratch/fresh-verification-kompiled"
raw_log=/tmp/audit-work/nonvacuity-kprove.raw.log
status=0

printf 'COMMAND: bash /audit-output/evidence/07_nonvacuity.sh\n'
printf 'MUTATION: force the loop negative accumulator to negFold(VS,A)+1\n'
printf 'SATISFYING COUNTEREXAMPLE: VS=[], A=0, B=0, OLD=0\n'
printf 'allInts(.ValSeq)=true, A<=0=true, B>=0=true\n'
printf 'real empty-loop largest_negative=0\n'
printf 'mutated K postcondition largest_negative=negFold(.ValSeq,0)+1=1\n'

cp /audit-output/evidence/spec-vacuity.k "$scratch/spec-vacuity.k"

printf 'RUN: kprove spec-vacuity.k --definition fresh-verification-kompiled --spec-module SPEC-VACUITY --dry-run\n'
(
  cd "$scratch" &&
  kprove spec-vacuity.k \
    --definition fresh-verification-kompiled \
    --spec-module SPEC-VACUITY \
    --dry-run
)
dry_status=$?
printf 'EXIT mutation dry-run: %d\n' "$dry_status"
if [[ "$dry_status" -ne 0 ]]; then
  status=1
fi

printf 'RUN: timeout 180 kprove spec-vacuity.k --definition fresh-verification-kompiled --spec-module SPEC-VACUITY\n'
(
  cd "$scratch" &&
  timeout 180 kprove spec-vacuity.k \
    --definition fresh-verification-kompiled \
    --spec-module SPEC-VACUITY
) >"$raw_log" 2>&1
proof_status=$?
sed -n '1,360p' "$raw_log"
printf 'EXIT false mutation proof: %d\n' "$proof_status"

if [[ "$proof_status" -eq 0 || "$proof_status" -eq 124 ]]; then
  status=1
fi
if ! rg -q 'WarnStuckClaimState' "$raw_log"; then
  printf 'EXPECTED WarnStuckClaimState: absent\n'
  status=1
else
  printf 'EXPECTED WarnStuckClaimState: present\n'
fi
if rg -qi 'parse error|could not find|no such file|kompile.*error|missing hook' "$raw_log"; then
  printf 'UNRELATED build/parser failure marker: present\n'
  status=1
else
  printf 'UNRELATED build/parser failure marker: absent\n'
fi

printf 'FINAL EXIT: %d\n' "$status"
exit "$status"
