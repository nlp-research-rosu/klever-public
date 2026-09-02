#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/reconstruction
definition="$scratch/verification-haskell-kompiled"
export PATH="/home/agent/.nix-profile/bin:$PATH"
printf 'COMMAND: bash /audit-output/evidence/stage3_prove.sh\n'
cp /audit-output/evidence/spec-labeled.k "$scratch/spec-labeled.k"

run_proof() {
  local label="$1"
  shift
  printf '\nTARGET: %s\n' "$label"
  printf 'COMMAND: cd %s &&' "$scratch"
  printf ' %q' "$@"
  printf '\n'
  local output
  output="$(cd "$scratch" && "$@" 2>&1)"
  local command_status=$?
  printf '%s\n' "$output"
  printf 'kprove_exit=%s\n' "$command_status"
  local top_status=1
  if printf '%s\n' "$output" | rg -x '#Top' >/dev/null; then
    top_status=0
  fi
  printf 'exact_top_line=%s\n' "$((1 - top_status))"
  if [[ "$command_status" != 0 || "$top_status" != 0 ]]; then
    return 1
  fi
  return 0
}

final_status=0
run_proof original-all \
  kprove spec.k \
  --definition "$definition" \
  --spec-module SPEC \
  || final_status=1

run_proof loop-invariant \
  kprove spec-labeled.k \
  --definition "$definition" \
  --spec-module SPEC-LABELED \
  --claims SPEC-LABELED.loop-invariant \
  || final_status=1

run_proof entry-general-with-proved-invariant \
  kprove spec-labeled.k \
  --definition "$definition" \
  --spec-module SPEC-LABELED \
  --claims SPEC-LABELED.loop-invariant,SPEC-LABELED.entry-general \
  || final_status=1

run_proof entry-zero-with-proved-invariant \
  kprove spec-labeled.k \
  --definition "$definition" \
  --spec-module SPEC-LABELED \
  --claims SPEC-LABELED.loop-invariant,SPEC-LABELED.entry-zero \
  || final_status=1

run_proof entry-five-with-proved-invariant \
  kprove spec-labeled.k \
  --definition "$definition" \
  --spec-module SPEC-LABELED \
  --claims SPEC-LABELED.loop-invariant,SPEC-LABELED.entry-five \
  || final_status=1

printf '\nSCRIPT_EXIT=%s\n' "$final_status"
exit "$final_status"
