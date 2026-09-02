#!/usr/bin/env bash
set -uo pipefail

WORK=/tmp/audit-work/run-002
EVIDENCE=/audit-output/evidence

run_ok() {
  local log=$1
  shift
  (
    printf 'COMMAND:'
    printf ' %q' "$@"
    printf '\n'
    "$@"
    local status=$?
    printf 'EXIT_STATUS: %s\n' "$status"
    exit "$status"
  ) 2>&1 | tee "$log"
  local pipeline_status=${PIPESTATUS[0]}
  if [[ "$pipeline_status" -ne 0 ]]; then
    return "$pipeline_status"
  fi
}

run_expected_failure() {
  local log=$1
  shift
  (
    printf 'COMMAND:'
    printf ' %q' "$@"
    printf '\n'
    "$@"
    local status=$?
    printf 'KPROVE_EXIT_STATUS: %s\n' "$status"
    if [[ "$status" -eq 0 ]]; then
      printf '%s\n' 'UNEXPECTED_SUCCESS'
      exit 1
    fi
    printf '%s\n' 'EXPECTED_NONZERO_PROOF_FAILURE'
    exit 0
  ) 2>&1 | tee "$log"
  local pipeline_status=${PIPESTATUS[0]}
  if [[ "$pipeline_status" -ne 0 ]]; then
    return "$pipeline_status"
  fi
}

run_ok "$EVIDENCE/stage1/provenance-check.log" \
  python3 "$EVIDENCE/stage1/provenance_check.py"
run_ok "$EVIDENCE/stage1/generation-record-inspection.log" \
  python3 "$EVIDENCE/stage1/generation_record_inspect.py"

(
  cd "$WORK" || exit 1
  printf '%s\n' 'COMMAND: python3 py2mpy.py solution.py > regenerated-solution.mpy'
  python3 py2mpy.py solution.py > regenerated-solution.mpy
  translate_status=$?
  printf 'TRANSLATOR_EXIT_STATUS: %s\n' "$translate_status"
  printf '%s\n' 'COMMAND: cmp -s regenerated-solution.mpy solution.mpy'
  cmp -s regenerated-solution.mpy solution.mpy
  compare_status=$?
  printf 'CMP_EXIT_STATUS: %s\n' "$compare_status"
  sha256sum solution.py solution.mpy regenerated-solution.mpy py2mpy.py
  exit "$compare_status"
) 2>&1 | tee "$EVIDENCE/stage2/translation-identity.log"
translation_pipeline_status=${PIPESTATUS[0]}
if [[ "$translation_pipeline_status" -ne 0 ]]; then
  exit "$translation_pipeline_status"
fi

run_ok "$EVIDENCE/stage2/differential-test.log" \
  python3 "$EVIDENCE/stage2/differential_test.py"

(
  cd "$WORK" || exit 1
  run_ok "$EVIDENCE/stage3/tool-versions.log" kompile --version
  run_ok "$EVIDENCE/stage3/kompile-llvm.log" \
    kompile reference-semantics/semantics.k \
    --backend llvm \
    --main-module MPY-KRUN \
    --syntax-module MPY-SYNTAX \
    --output-definition audit-runtime-rebuild-kompiled
  run_ok "$EVIDENCE/stage3/krun-smoke.log" \
    krun smoke.mpy --definition audit-runtime-rebuild-kompiled
  run_ok "$EVIDENCE/stage3/kompile-haskell.log" \
    kompile verification.k \
    --backend haskell \
    --main-module VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition audit-verification-rebuild-kompiled
  run_ok "$EVIDENCE/stage3/kprove-loop.log" \
    kprove spec-loop.k \
    --definition audit-verification-rebuild-kompiled \
    --spec-module SPEC-LOOP
  run_ok "$EVIDENCE/stage3/kprove-all.log" \
    kprove spec.k \
    --definition audit-verification-rebuild-kompiled \
    --spec-module SPEC
)
stage3_status=$?
if [[ "$stage3_status" -ne 0 ]]; then
  exit "$stage3_status"
fi

run_ok "$EVIDENCE/stage4/program-term-check.log" \
  python3 "$EVIDENCE/stage4/program_term_check.py"
run_ok "$EVIDENCE/stage4/ground-python-witness.log" \
  python3 "$EVIDENCE/stage4/ground_python_witness.py"
(
  cd "$WORK" || exit 1
  run_ok "$EVIDENCE/stage4/kprove-ground-witnesses.log" \
    kprove spec-ground-entry.k \
    --definition audit-verification-rebuild-kompiled \
    --spec-module SPEC-GROUND-ENTRY
  run_ok "$EVIDENCE/stage4/body-mutation-build.log" \
    kompile verification-body-mut.k \
    --backend haskell \
    --main-module VERIFICATION-BODY-MUT \
    --syntax-module MPY-SYNTAX \
    --output-definition audit-body-mut-rebuild-kompiled
  run_expected_failure "$EVIDENCE/stage4/body-mutation-proof.log" \
    kprove spec-body-mut.k \
    --definition audit-body-mut-rebuild-kompiled \
    --spec-module SPEC-BODY-MUT
)
stage4_status=$?
if [[ "$stage4_status" -ne 0 ]]; then
  exit "$stage4_status"
fi

run_ok "$EVIDENCE/stage5/rule-inventory-build.log" \
  python3 "$EVIDENCE/stage5/build_rule_inventory.py"

(
  cd "$WORK" || exit 1
  run_ok "$EVIDENCE/stage6/vacuity-dry-run.log" \
    kprove spec-vacuity.k \
    --definition audit-verification-rebuild-kompiled \
    --spec-module SPEC-VACUITY \
    --dry-run \
    --output none
  run_expected_failure "$EVIDENCE/stage6/vacuity-proof.log" \
    kprove spec-vacuity.k \
    --definition audit-verification-rebuild-kompiled \
    --spec-module SPEC-VACUITY
)
stage6_status=$?
if [[ "$stage6_status" -ne 0 ]]; then
  exit "$stage6_status"
fi

printf '%s\n' 'ALL_CAPTURED_CHECKS=PASS'
