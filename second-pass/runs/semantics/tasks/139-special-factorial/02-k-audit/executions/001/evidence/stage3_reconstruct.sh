#!/usr/bin/env bash
set -u

task_dir=/tmp/audit-work/139-special-factorial
evidence_dir=/audit-output/evidence

run_logged() {
  label=$1
  shift
  log="$evidence_dir/stage3_${label}.log"
  (
    printf '$'
    printf ' %q' "$@"
    printf '\n'
    timeout 900 "$@"
    rc=$?
    printf '[exit %d]\n' "$rc"
    exit "$rc"
  ) > "$log" 2>&1
  rc=$?
  printf '%s exit=%d log=%s\n' "$label" "$rc" "$log"
  return "$rc"
}

cd "$task_dir" || exit 2

printf 'STAGE 3 CLEAN RECONSTRUCTION\n'
if test -e runtime-kompiled || test -e verification-kompiled; then
  printf 'Refusing to reuse an existing compiled definition.\n'
  exit 2
fi

run_logged concrete_build \
  kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
concrete_build_rc=$?

run_logged concrete_run \
  krun run.mpy \
  --definition runtime-kompiled \
  --output pretty
concrete_run_rc=$?

run_logged proof_build \
  kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
proof_build_rc=$?

run_logged prove_loop \
  kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.special-factorial-loop \
  --output pretty
prove_loop_rc=$?

run_logged prove_entry \
  kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.special-factorial-correct \
  --output pretty
prove_entry_rc=$?

run_logged prove_all \
  kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --output pretty
prove_all_rc=$?

printf 'summary concrete_build=%d concrete_run=%d proof_build=%d loop=%d entry=%d all=%d\n' \
  "$concrete_build_rc" "$concrete_run_rc" "$proof_build_rc" \
  "$prove_loop_rc" "$prove_entry_rc" "$prove_all_rc"

if (( concrete_build_rc || concrete_run_rc || proof_build_rc ||
      prove_loop_rc || prove_entry_rc || prove_all_rc )); then
  exit 1
fi
