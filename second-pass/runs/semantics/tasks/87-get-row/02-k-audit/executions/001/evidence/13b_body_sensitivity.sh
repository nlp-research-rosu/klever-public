#!/usr/bin/env bash
set -u

work=/tmp/audit-work/87-get-row
original=/audit-output/evidence/solution.original.mpy
mutant=/audit-output/evidence/solution.body-mutant.mpy

restore_original() {
  cp -a "$original" "$work/solution.mpy"
}
trap restore_original EXIT

echo "AUDIT COMMAND: bash /audit-output/evidence/13b_body_sensitivity.sh"
cp -a "$mutant" "$work/solution.mpy"
echo "Active solution.mpy during fresh proof build:"
sha256sum "$work/solution.mpy"
tail -n 4 "$work/solution.mpy"

echo "BUILD: kompile verification.k --backend haskell --main-module GET-ROW-VERIFICATION --syntax-module MPY-SYNTAX --output-definition body-sensitivity-verification-kompiled"
(
  cd "$work" &&
    kompile verification.k \
      --backend haskell \
      --main-module GET-ROW-VERIFICATION \
      --syntax-module MPY-SYNTAX \
      --output-definition body-sensitivity-verification-kompiled
)
build_status=$?
echo "BUILD_EXIT=$build_status"
if [[ "$build_status" -ne 0 ]]; then
  exit "$build_status"
fi

echo "PROVE: kprove spec.k --definition body-sensitivity-verification-kompiled --spec-module GET-ROW-SPEC"
(
  cd "$work" &&
    kprove spec.k \
      --definition body-sensitivity-verification-kompiled \
      --spec-module GET-ROW-SPEC
)
proof_status=$?
echo "PROOF_EXIT=$proof_status"
exit "$proof_status"
