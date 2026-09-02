#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/case91
definition="$scratch/audit-verification-kompiled"
overall=0

run_kast() {
  local source=$1
  local output=$2
  local log=$3
  (
    printf 'COMMAND: kast %q --definition %q --module VERIFICATION --sort Module --output kore\n' \
      "$source" "$definition"
    printf 'WORKDIR: %s\n' "$scratch"
    (
      cd "$scratch"
      kast "$source" \
        --definition "$definition" \
        --module VERIFICATION \
        --sort Module \
        --output kore \
        > "$output"
    )
    ec=$?
    printf 'EXIT_STATUS=%d\n' "$ec"
    exit "$ec"
  ) > "$log" 2>&1
  ec=$?
  if [[ $ec -ne 0 ]]; then overall=1; fi
}

run_kast solution.mpy \
  "$scratch/audit-solution.kore" \
  /audit-output/evidence/stage4_kast_solution.log
run_kast proof-program.mpy \
  "$scratch/audit-proof-program.kore" \
  /audit-output/evidence/stage4_kast_proof_program.log

(
  printf 'COMMAND: cmp -s %q %q\n' \
    "$scratch/audit-solution.kore" \
    "$scratch/audit-proof-program.kore"
  cmp -s "$scratch/audit-solution.kore" "$scratch/audit-proof-program.kore"
  ec=$?
  printf 'EXIT_STATUS=%d\n' "$ec"
  sha256sum "$scratch/audit-solution.kore" "$scratch/audit-proof-program.kore"
  if [[ $ec -ne 0 ]]; then
    diff -u "$scratch/audit-solution.kore" "$scratch/audit-proof-program.kore"
  fi
  exit "$ec"
) > /audit-output/evidence/stage4_kore_identity.log 2>&1
ec=$?
if [[ $ec -ne 0 ]]; then overall=1; fi

printf 'FINAL_STATUS=%d\n' "$overall"
exit "$overall"
