#!/usr/bin/env bash
set -uo pipefail

evidence_dir=/audit-output/evidence
scratch_dir=/tmp/audit-work/88-sort-array
log_file="$evidence_dir/reconstruction.log"
runtime_definition="$scratch_dir/runtime-audit-kompiled"
proof_definition="$scratch_dir/verification-audit-kompiled"

run() {
  local command_text=$1
  printf '\n$ %s\n' "$command_text"
  bash -o pipefail -c "$command_text"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

{
  run "kompile --version" || exit $?
  run "kprove --version" || exit $?
  if [[ -d "$runtime_definition" ]]; then
    run "rm -rf -- $runtime_definition" || exit $?
  fi
  if [[ -d "$proof_definition" ]]; then
    run "rm -rf -- $proof_definition" || exit $?
  fi
  run "kompile $scratch_dir/reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition $runtime_definition" || exit $?
  run "krun $scratch_dir/concrete_tests.mpy --definition $runtime_definition" || exit $?
  run "kompile $scratch_dir/verification.k --backend haskell --main-module VERIFICATION --syntax-module VERIFICATION --output-definition $proof_definition" || exit $?
  run "kprove $scratch_dir/spec.k --definition $proof_definition --spec-module SPEC" || exit $?
  for label in empty singleton odd even; do
    run "kprove $evidence_dir/spec-labeled.k -I $scratch_dir --definition $proof_definition --spec-module SPEC-LABELED --claims $label" || exit $?
  done
  run "kast $scratch_dir/regenerated-solution.mpy --definition $proof_definition --module VERIFICATION --sort Module --output pretty > $scratch_dir/normalized-solution.k" || exit $?
  run "python3 $evidence_dir/generate_pinning_spec.py $scratch_dir/normalized-solution.k > $scratch_dir/pinning.k" || exit $?
  run "kprove $scratch_dir/pinning.k --definition $proof_definition --spec-module PINNING" || exit $?
} 2>&1 | tee "$log_file"
status=${PIPESTATUS[0]}
printf 'SCRIPT_EXIT=%d\n' "$status" | tee -a "$log_file"
exit "$status"
