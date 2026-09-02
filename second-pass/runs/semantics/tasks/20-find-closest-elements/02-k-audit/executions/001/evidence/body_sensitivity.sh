#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/reconstruction
original="$scratch/solution.mpy"
backup="$scratch/solution.mpy.audit-original"
mutation=/audit-output/evidence/solution-body-mutation.mpy
definition="$scratch/verification-body-mutated-kompiled"

cp "$original" "$backup"
restore() {
  mv "$backup" "$original"
}
trap restore EXIT

sed \
  's/Return(TupleExpr(Name("best_low"), Name("best_high")))/Return(TupleExpr(Name("best_high"), Name("best_low")))/' \
  "$backup" >"$original"
cp "$original" "$mutation"

echo "mutation: reverse the function's returned pair in the submitted program artifact"
sha256sum "$backup" "$original" "$mutation"
if cmp -s "$backup" "$original"; then
  echo "mutation did not change solution.mpy"
  exit 65
fi

echo "command: kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-body-mutated-kompiled"
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-body-mutated-kompiled
build_status=$?
printf 'build_exit_status=%s\n' "$build_status"
if (( build_status != 0 )); then
  exit "$build_status"
fi

echo "command: kprove spec.k --definition verification-body-mutated-kompiled --spec-module SPEC"
kprove spec.k \
  --definition verification-body-mutated-kompiled \
  --spec-module SPEC
proof_status=$?
printf 'proof_exit_status=%s\n' "$proof_status"
exit "$proof_status"
