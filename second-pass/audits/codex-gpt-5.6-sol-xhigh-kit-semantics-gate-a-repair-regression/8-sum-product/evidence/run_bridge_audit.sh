#!/usr/bin/env bash
set -u

SCRATCH=/tmp/audit-work/reconstruction
EVIDENCE=/audit-output/evidence/logs
export PATH="/home/agent/.nix-profile/bin:$PATH"

run_bounded() {
  name=$1
  shift
  full="$SCRATCH/$name.full.log"
  bounded="$EVIDENCE/$name.log"
  {
    printf '$'
    printf ' %q' "$@"
    printf '\n'
  } > "$bounded"
  "$@" > "$full" 2>&1
  status=$?
  lines=$(wc -l < "$full")
  {
    printf '[exit %d; output lines %d]\n' "$status" "$lines"
    if [ "$lines" -le 220 ]; then
      sed -n '1,220p' "$full"
    else
      sed -n '1,110p' "$full"
      printf '[... %d middle lines omitted ...]\n' "$((lines - 220))"
      tail -n 110 "$full"
    fi
  } >> "$bounded"
  sed -n '1,240p' "$bounded"
  return "$status"
}

cp /audit-output/evidence/spec-bridge-audit.k "$SCRATCH/spec-bridge-audit.k"
cd "$SCRATCH" || exit 1

run_bounded bridge_ground_base \
  kprove spec-bridge-audit.k \
  --definition audit-verification-base-kompiled \
  --spec-module BRIDGE-WITNESS-BASE || exit $?

run_bounded bridge_ground_extended \
  kprove spec-bridge-audit.k \
  --definition audit-verification-kompiled \
  --spec-module BRIDGE-WITNESS-EXTENDED || exit $?

run_bounded bridge_changed_context \
  kprove spec-bridge-audit.k \
  --definition audit-verification-kompiled \
  --spec-module BRIDGE-CONTEXT-WITNESS || exit $?

run_bounded bridge_body_mutation_dry_run \
  kprove spec-bridge-audit.k \
  --definition audit-verification-kompiled \
  --spec-module BRIDGE-BODY-MUTATION --dry-run || exit $?

run_bounded bridge_body_mutation \
  kprove spec-bridge-audit.k \
  --definition audit-verification-kompiled \
  --spec-module BRIDGE-BODY-MUTATION
mutation_status=$?
if [ "$mutation_status" -eq 0 ]; then
  printf '%s\n' 'UNEXPECTED: changed-body old result proved' >&2
  exit 1
fi
if ! rg -q 'WarnStuckClaimState' "$EVIDENCE/bridge_body_mutation.log"; then
  printf '%s\n' 'UNEXPECTED: changed body failed without stuck claim' >&2
  exit 1
fi
printf 'expected_changed_body_exit=%d; stuck_claim=yes\n' "$mutation_status"
