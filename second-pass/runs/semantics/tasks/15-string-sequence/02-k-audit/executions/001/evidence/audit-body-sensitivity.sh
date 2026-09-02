#!/usr/bin/env bash
set -uo pipefail

target=/tmp/audit-work/body-sensitivity
mkdir -p "$target/reference-semantics"
cp -a /tmp/audit-work/reconstruction/reference-semantics/. "$target/reference-semantics/"
cp -a /tmp/audit-work/reconstruction/verification.k "$target/verification.k"
cp -a /tmp/audit-work/reconstruction/spec-positive-only.k "$target/spec-positive-only.k"
cp -a /audit-output/evidence/solution-body-mutant.mpy "$target/solution.mpy"

cd "$target"
echo "COMMAND: cmp mutated solution.mpy against submitted scratch solution.mpy (difference is expected)"
cmp solution.mpy /tmp/audit-work/reconstruction/solution.mpy
cmp_status=$?
echo "CMP_EXIT=$cmp_status"
if (( cmp_status == 0 )); then
  echo "ERROR: mutation did not change the body"
  exit 2
fi
sha256sum solution.mpy /tmp/audit-work/reconstruction/solution.mpy
echo "Mutated final return:"
grep -n 'Return(Str("MUTATED"))' solution.mpy

echo "COMMAND: kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled"
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
status=$?
echo "KOMPILE_EXIT=$status"
if (( status != 0 )); then exit "$status"; fi

echo "COMMAND: kprove spec-positive-only.k --definition verification-kompiled --spec-module AUDIT-POSITIVE-ONLY"
kprove spec-positive-only.k \
  --definition verification-kompiled \
  --spec-module AUDIT-POSITIVE-ONLY
status=$?
echo "KPROVE_EXIT=$status"
exit "$status"
