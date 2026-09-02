#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/reconstruction
original="$scratch/verification.k"
backup="$scratch/verification.k.audit-original"
mutation=/audit-output/evidence/verification-operational-mutation.k
haskell_definition="$scratch/verification-opmut-kompiled"
llvm_definition="$scratch/verification-opmut-llvm-kompiled"

cp "$original" "$backup"
restore() {
  mv "$backup" "$original"
}
trap restore EXIT

# Change the displaced loop computation so every candidate gap is compared with
# best_high-best_high (zero) instead of the current best gap.
sed \
  's/CmpOp("<", BinOp("-", Name("best_high"), Name("best_low"))))/CmpOp("<", BinOp("-", Name("best_high"), Name("best_high"))))/' \
  "$backup" >"$original"
cp "$original" "$mutation"

echo "mutation: loop update compares candidate gap with best_high-best_high"
sha256sum "$backup" "$original" "$mutation"
if cmp -s "$backup" "$original"; then
  echo "mutation did not change verification.k"
  exit 65
fi

echo "command: kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-opmut-kompiled"
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-opmut-kompiled
build_haskell_status=$?
printf 'haskell_build_exit_status=%s\n' "$build_haskell_status"
if (( build_haskell_status != 0 )); then
  exit "$build_haskell_status"
fi

echo "command: kprove spec.k --definition verification-opmut-kompiled --spec-module SPEC"
kprove spec.k \
  --definition verification-opmut-kompiled \
  --spec-module SPEC
proof_status=$?
printf 'mutated_body_proof_exit_status=%s\n' "$proof_status"
if (( proof_status != 0 )); then
  exit "$proof_status"
fi

echo "command: kompile verification.k --backend llvm --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-opmut-llvm-kompiled"
kompile verification.k \
  --backend llvm \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-opmut-llvm-kompiled
build_llvm_status=$?
printf 'llvm_build_exit_status=%s\n' "$build_llvm_status"
if (( build_llvm_status != 0 )); then
  exit "$build_llvm_status"
fi

echo "command: krun operational_mutation_witness.mpy --definition verification-opmut-llvm-kompiled --output pretty"
krun /audit-output/evidence/operational_mutation_witness.mpy \
  --definition verification-opmut-llvm-kompiled \
  --output pretty
bridge_run_status=$?
printf 'bridge_enabled_witness_exit_status=%s\n' "$bridge_run_status"
if (( bridge_run_status == 0 )); then
  echo "heap-ref literal call remains on fixed semantics: the bridge only matches the spec's unboxed-list boundary"
else
  echo "bridge affected the heap-ref literal call (non-zero execution status)"
fi
echo "sensitivity result: the unboxed-list positive proof stayed #Top after the displaced loop computation changed"
exit 0
