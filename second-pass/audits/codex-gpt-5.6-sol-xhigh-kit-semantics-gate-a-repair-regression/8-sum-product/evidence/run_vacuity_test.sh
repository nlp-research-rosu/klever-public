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
    if [ "$lines" -le 240 ]; then
      sed -n '1,240p' "$full"
    else
      sed -n '1,120p' "$full"
      printf '[... %d middle lines omitted ...]\n' "$((lines - 240))"
      tail -n 120 "$full"
    fi
  } >> "$bounded"
  sed -n '1,260p' "$bounded"
  return "$status"
}

cp /audit-output/evidence/spec-audit-vacuity.k \
  "$SCRATCH/spec-audit-vacuity.k"
cd "$SCRATCH" || exit 1

run_bounded vacuity_dry_run \
  kprove spec-audit-vacuity.k \
  --definition audit-verification-base-kompiled \
  --spec-module SPEC-AUDIT-VACUITY --dry-run
dry_status=$?
if [ "$dry_status" -ne 0 ]; then
  exit "$dry_status"
fi

run_bounded vacuity_proof \
  kprove spec-audit-vacuity.k \
  --definition audit-verification-base-kompiled \
  --spec-module SPEC-AUDIT-VACUITY
proof_status=$?
if [ "$proof_status" -eq 0 ]; then
  printf '%s\n' 'UNEXPECTED: false mutation proved' >&2
  exit 1
fi

if ! rg -q 'WarnStuckClaimState' "$EVIDENCE/vacuity_proof.log"; then
  printf '%s\n' 'UNEXPECTED: mutation failed without a stuck claim' >&2
  exit 1
fi

printf 'expected_false_mutation_exit=%d; stuck_claim=yes\n' "$proof_status"
exit 0
