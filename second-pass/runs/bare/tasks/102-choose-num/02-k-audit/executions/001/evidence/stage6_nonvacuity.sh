#!/usr/bin/env bash
set -u

LOG=/audit-output/evidence/stage6-nonvacuity.log
RAW=/audit-output/evidence/stage6-vacuity-proof.raw.log
DRY=/audit-output/evidence/stage6-vacuity-dry-run.raw.log
exec > >(tee "$LOG") 2>&1

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

cd /tmp/audit-work || exit 1
status=0
printf 'STAGE 6 FRESH NON-VACUITY TEST\n'
run cmp -s spec-vacuity-fresh.k /audit-output/evidence/spec-vacuity-fresh.k || status=1
run python3 /audit-output/evidence/concrete_oracle.py 1 2 2 || status=1
run python3 -c \
  'x,y=1,2; actual=2; mutated=y+2; print(f"witness=({x},{y}) actual={actual} mutated_obligation={mutated} false={actual != mutated}"); assert x>0 and y>0 and x<=y and y%2==0 and actual!=mutated' \
  || status=1

printf '$ kprove spec-vacuity-fresh.k --definition proof-kompiled --spec-module SPEC-VACUITY-FRESH --dry-run > %s 2>&1\n' "$DRY"
kprove spec-vacuity-fresh.k \
  --definition proof-kompiled \
  --spec-module SPEC-VACUITY-FRESH \
  --dry-run \
  > "$DRY" 2>&1
dry_status=$?
printf '[exit %d]\n' "$dry_status"
run wc -c "$DRY"
run sed -n 1,30p "$DRY"
if (( dry_status != 0 )); then status=1; fi

printf '$ kprove spec-vacuity-fresh.k --definition proof-kompiled --spec-module SPEC-VACUITY-FRESH 2>&1 | tee %s\n' "$RAW"
kprove spec-vacuity-fresh.k \
  --definition proof-kompiled \
  --spec-module SPEC-VACUITY-FRESH \
  2>&1 | tee "$RAW"
proof_status=${PIPESTATUS[0]}
printf '[exit %d]\n' "$proof_status"

if (( proof_status == 0 )); then
  printf 'ERROR: deliberately false mutation unexpectedly closed\n'
  status=1
else
  printf 'expected_nonzero_proof_status=%d\n' "$proof_status"
fi
run rg -n 'WarnStuckClaimState' "$RAW" || status=1
run rg -n 'implication check between the conditions has failed|cannot be rewritten further' "$RAW" || status=1
if rg -q '^#Top$' "$RAW"; then
  printf 'ERROR: raw mutation log contains #Top\n'
  status=1
else
  printf 'raw_mutation_contains_top=false\n'
fi

printf 'stage6_status=%d\n' "$status"
exit "$status"
