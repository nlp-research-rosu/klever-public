#!/usr/bin/env bash
set -u

SOURCE=/tmp/audit-work/source
SCRATCH=/tmp/audit-work/adequacy
PROOF_DEF=/tmp/audit-work/reconstruction/verification-haskell

run_shell() {
  local command_text="$1"
  printf 'COMMAND: %s\n' "$command_text"
  bash -o pipefail -c "$command_text"
  local status=$?
  printf 'EXIT_STATUS: %s\n\n' "$status"
  return "$status"
}

run_shell "mkdir -p '$SCRATCH'"
run_shell "cp /audit-output/evidence/stage4/macro-program.mpy '$SCRATCH/macro-program.mpy'"
run_shell "cp /audit-output/evidence/stage4/spec-ground-values.k '$SOURCE/spec-ground-values.k'"

printf 'SOURCE-TO-CLAIM PINNING BY EXPANDED PARSE TERM\n'
run_shell "kast '$SOURCE/solution.mpy' --definition '$PROOF_DEF' --module VERIFICATION --sort Program --expand-macros --output kore > '$SCRATCH/solution-expanded.kore'"
solution_kast_status=$?
run_shell "kast '$SCRATCH/macro-program.mpy' --definition '$PROOF_DEF' --module VERIFICATION --sort Program --expand-macros --output kore > '$SCRATCH/claim-program-expanded.kore'"
claim_kast_status=$?
run_shell "cmp --silent '$SCRATCH/solution-expanded.kore' '$SCRATCH/claim-program-expanded.kore'"
pinning_status=$?
run_shell "sha256sum '$SCRATCH/solution-expanded.kore' '$SCRATCH/claim-program-expanded.kore'"

printf 'GROUND SUBSTITUTIONS FOR CLAIMED SUMMARY VALUES\n'
run_shell "cd '$SOURCE' && kprove spec-ground-values.k --definition '$PROOF_DEF' --spec-module SPEC-GROUND-VALUES"
ground_status=$?

printf 'INDEPENDENT PYTHON VALUES FOR THE SAME ENTRY INPUTS\n'
python_status=0
for n in -100 0 79 771 7778; do
  run_shell "python3 /audit-output/evidence/stage3/compare_concrete.py '$n'"
  status=$?
  if [[ $status -ne 0 ]]; then
    python_status=1
  fi
done

printf 'RELEVANT SOURCE AND CLAIM TEXT\n'
run_shell "nl -ba '$SOURCE/solution.mpy'"
run_shell "nl -ba '$SOURCE/spec.k'"
run_shell "nl -ba '$SOURCE/verification.k'"
run_shell "sed -n '1,240p' /audit-output/evidence/stage4/satisfying-states.txt"

printf 'SUMMARY solution_kast=%s claim_kast=%s pinning=%s ground=%s python=%s\n' \
  "$solution_kast_status" "$claim_kast_status" "$pinning_status" "$ground_status" "$python_status"
if [[ $solution_kast_status -ne 0 || $claim_kast_status -ne 0 || $pinning_status -ne 0 || $ground_status -ne 0 || $python_status -ne 0 ]]; then
  exit 1
fi
exit 0

