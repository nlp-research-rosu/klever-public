#!/usr/bin/env bash
set -u

evidence_dir=/audit-output/evidence
work_dir=/tmp/audit-work/race41

run_logged() {
  log_name=$1
  shift
  {
    printf 'COMMAND:'
    printf ' %q' "$@"
    printf '\n'
    "$@"
    command_status=$?
    printf '\nEXIT_STATUS: %d\n' "$command_status"
    return "$command_status"
  } > "$evidence_dir/$log_name" 2>&1
}

mkdir -p "$work_dir"

run_logged provenance.log python3 "$evidence_dir/provenance_check.py" || exit 10

run_logged scratch_copy.log \
  cp \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/semantic.k \
  /candidate/verification.k \
  /candidate/spec.k \
  /candidate/prove.sh \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  "$work_dir/" || exit 11

run_logged scratch_manifest.log \
  find "$work_dir" -maxdepth 1 -type f -printf '%f %s bytes\n' || exit 12

run_logged regenerate_mpy.log \
  bash -c 'python3 /reference/py2mpy.py /tmp/audit-work/race41/solution.py > /tmp/audit-work/race41/solution.regenerated.mpy' ||
  exit 13

run_logged mpy_byte_identity.log \
  cmp -s "$work_dir/solution.mpy" "$work_dir/solution.regenerated.mpy" || exit 14

run_logged differential.log python3 "$evidence_dir/differential_test.py" || exit 15

run_logged kompile_llvm.log \
  kompile "$work_dir/semantic.k" \
  --backend llvm \
  --main-module SEMANTIC \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition "$work_dir/semantic-llvm-kompiled" || exit 20

for value in 0 1 3 10 41; do
  run_logged "krun_n_${value}.log" \
    krun "$work_dir/solution.mpy" \
    --definition "$work_dir/semantic-llvm-kompiled" \
    "-cN=$value" || exit 21
done

run_logged concrete_comparison.log \
  python3 "$evidence_dir/check_concrete_results.py" || exit 22

run_logged kompile_haskell.log \
  kompile "$work_dir/verification.k" \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition "$work_dir/verification-kompiled" || exit 30

run_logged kprove_positive.log \
  kprove "$work_dir/spec.k" \
  --definition "$work_dir/verification-kompiled" \
  --spec-module SPEC || exit 31

run_logged copy_vacuity_spec.log \
  cp "$evidence_dir/spec-vacuity.k" "$work_dir/spec-vacuity.k" || exit 40
if run_logged kprove_vacuity.log \
  kprove "$work_dir/spec-vacuity.k" \
  --definition "$work_dir/verification-kompiled" \
  --spec-module SPEC-VACUITY; then
  exit 41
fi

run_logged copy_body_mutation_spec.log \
  cp "$evidence_dir/spec-body-mutation.k" "$work_dir/spec-body-mutation.k" || exit 42
if run_logged kprove_body_mutation.log \
  kprove "$work_dir/spec-body-mutation.k" \
  --definition "$work_dir/verification-kompiled" \
  --spec-module SPEC-BODY-MUTATION; then
  exit 43
fi

printf 'AUDIT_SCRIPT_STATUS: 0\n'
