#!/usr/bin/env bash
set +e

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n\n' "$status"
  return "$status"
}

cd /tmp/audit-work/109-move-one-ball/candidate || exit 90
export PATH="$HOME/.nix-profile/bin:$PATH"

run python3 -c 'from solution import move_one_ball; print(move_one_ball([]))'
python_status=$?

run kprove spec-vacuity-auditor.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY-AUDITOR \
  --dry-run
dry_status=$?

run kprove spec-vacuity-auditor.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY-AUDITOR \
  --output pretty
proof_status=$?

printf 'satisfying_witness_python_status=%d\n' "$python_status"
printf 'mutation_dry_run_status=%d\n' "$dry_status"
printf 'mutation_proof_status=%d\n' "$proof_status"

if (( python_status != 0 || dry_status != 0 || proof_status == 0 )); then
  exit 1
fi
