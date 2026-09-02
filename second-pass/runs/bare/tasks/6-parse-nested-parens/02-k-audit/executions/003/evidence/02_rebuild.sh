#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/candidate
run_root=/tmp/audit-work/runs/rebuild2
semantic_definition="$run_root/semantic-kompiled"
verification_definition="$run_root/verification-kompiled"
isolated_spec="$scratch/isolated-specs.k"

run_step() {
  local label="$1"
  shift
  echo "COMMAND[$label]: $*"
  "$@"
  local step_status=$?
  echo "EXIT[$label]: $step_status"
  return "$step_status"
}

cd "$scratch" || exit 90
mkdir -p "$run_root"

overall_status=0
run_step "tool-kompile-version" kompile --version || overall_status=1
run_step "tool-kprove-version" kprove --version || overall_status=1
run_step "tool-krun-version" krun --version || overall_status=1

run_step "kompile-llvm" \
  kompile semantic.k \
  --main-module MPY-SEMANTICS \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition "$semantic_definition" || overall_status=1

run_step "python-oracles" \
  python3 /audit-output/evidence/02_concrete_oracles.py || overall_status=1

run_step "krun-normal" \
  krun solution.mpy \
  --definition "$semantic_definition" \
  -cINPUT='"(()()) ((())) () ((())()())"' || overall_status=1

run_step "krun-branch-boundary" \
  krun solution.mpy \
  --definition "$semantic_definition" \
  -cINPUT='"()()"' || overall_status=1

run_step "krun-empty" \
  krun solution.mpy \
  --definition "$semantic_definition" \
  -cINPUT='""' || overall_status=1

run_step "krun-repeated-separator" \
  krun solution.mpy \
  --definition "$semantic_definition" \
  -cINPUT='"()  (())"' || overall_status=1

run_step "kompile-haskell" \
  kompile verification.k \
  --main-module MPY-VERIFICATION \
  --syntax-module MPY-VERIFICATION \
  --backend haskell \
  --output-definition "$verification_definition" || overall_status=1

run_step "kprove-all-candidate-claims" \
  kprove spec.k \
  --definition "$verification_definition" \
  --spec-module SPEC || overall_status=1

run_step "kprove-claim-example" \
  kprove "$isolated_spec" \
  --definition "$verification_definition" \
  --spec-module AUDIT-SPEC-EXAMPLE || overall_status=1

run_step "kprove-claim-increasing" \
  kprove "$isolated_spec" \
  --definition "$verification_definition" \
  --spec-module AUDIT-SPEC-INCREASING || overall_status=1

run_step "kprove-claim-single" \
  kprove "$isolated_spec" \
  --definition "$verification_definition" \
  --spec-module AUDIT-SPEC-SINGLE || overall_status=1

echo "REBUILD_OVERALL_EXIT=$overall_status"
exit "$overall_status"
