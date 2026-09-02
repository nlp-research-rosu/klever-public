#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/proof || exit 90
audit_definition=/tmp/audit-work/proof/audit-haskell-kompiled

printf 'MUTATION WITNESS: BS=noBrackets(), rendered input="", mutated result=false, canonical/generated/K result=true\n'

printf 'COMMAND: kprove spec-vacuity-audit.k --definition %s --spec-module SPEC-VACUITY-AUDIT --dry-run\n' \
  "$audit_definition"
kprove spec-vacuity-audit.k \
  --definition "$audit_definition" \
  --spec-module SPEC-VACUITY-AUDIT \
  --dry-run
dry_exit=$?
printf 'false mutation dry-run/build exit=%s\n' "$dry_exit"
if (( dry_exit != 0 )); then
  exit 1
fi

printf 'COMMAND: kprove spec-vacuity-audit.k --definition %s --spec-module SPEC-VACUITY-AUDIT\n' \
  "$audit_definition"
kprove spec-vacuity-audit.k \
  --definition "$audit_definition" \
  --spec-module SPEC-VACUITY-AUDIT \
  > false-mutation-proof.out \
  2>&1
proof_exit=$?
sed -n '1,240p' false-mutation-proof.out
printf 'false mutation proof exit=%s (nonzero expected)\n' "$proof_exit"

grep -Fq 'WarnStuckClaimState' false-mutation-proof.out
stuck_exit=$?
printf 'expected stuck-claim diagnostic grep exit=%s\n' "$stuck_exit"
grep -Fq '#Top' false-mutation-proof.out
top_exit=$?
printf '#Top absence check grep exit=%s (1 expected)\n' "$top_exit"

if (( proof_exit == 0 || stuck_exit != 0 || top_exit == 0 )); then
  exit 1
fi
