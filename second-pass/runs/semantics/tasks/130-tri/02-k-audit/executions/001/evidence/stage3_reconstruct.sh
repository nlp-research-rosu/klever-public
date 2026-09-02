#!/usr/bin/env bash
set -u
set -o pipefail

audit_dir=/audit-output/evidence
work_dir=/tmp/audit-work/reconstruction
cd "$work_dir" || exit 90

echo '$ kompile --version'
kompile --version
echo "exit=$?"
echo '$ kprove --version'
kprove --version
echo "exit=$?"
echo '$ krun --version'
krun --version
echo "exit=$?"

echo '$ test ! -e runtime-kompiled && test ! -e verification-kompiled'
test ! -e runtime-kompiled && test ! -e verification-kompiled
fresh_rc=$?
echo "exit=$fresh_rc"

echo '$ cmp solution.mpy solution.regenerated.mpy'
cmp solution.mpy solution.regenerated.mpy
identity_rc=$?
echo "exit=$identity_rc"

echo '$ cp /audit-output/evidence/concrete_harness.mpy /tmp/audit-work/reconstruction/concrete_harness.mpy'
cp "$audit_dir/concrete_harness.mpy" "$work_dir/concrete_harness.mpy"
copy_rc=$?
echo "exit=$copy_rc"

echo '$ kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled'
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
runtime_build_rc=$?
echo "exit=$runtime_build_rc"

if [ "$runtime_build_rc" -eq 0 ]; then
  echo '$ krun concrete_harness.mpy --definition runtime-kompiled --output none'
  krun concrete_harness.mpy \
    --definition runtime-kompiled \
    --output none
  concrete_rc=$?
  echo "exit=$concrete_rc"
else
  concrete_rc=99
  echo 'SKIPPED concrete execution because runtime build failed'
  echo "exit=$concrete_rc"
fi

echo '$ kompile verification.k --backend haskell --main-module TRI-VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled'
kompile verification.k \
  --backend haskell \
  --main-module TRI-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
proof_build_rc=$?
echo "exit=$proof_build_rc"

if [ "$proof_build_rc" -eq 0 ]; then
  echo '$ kprove spec.k --definition verification-kompiled --spec-module TRI-LOOP-SPEC --output pretty'
  kprove spec.k \
    --definition verification-kompiled \
    --spec-module TRI-LOOP-SPEC \
    --output pretty
  loop_rc=$?
  echo "exit=$loop_rc"

  echo '$ kprove spec.k --definition verification-kompiled --spec-module TRI-CORRECT-SPEC --output pretty'
  kprove spec.k \
    --definition verification-kompiled \
    --spec-module TRI-CORRECT-SPEC \
    --output pretty
  entry_rc=$?
  echo "exit=$entry_rc"
else
  loop_rc=99
  entry_rc=99
  echo 'SKIPPED positive proof claims because proof build failed'
  echo "loop_exit=$loop_rc"
  echo "entry_exit=$entry_rc"
fi

echo "SUMMARY fresh=$fresh_rc identity=$identity_rc copy=$copy_rc runtime_build=$runtime_build_rc concrete=$concrete_rc proof_build=$proof_build_rc loop=$loop_rc entry=$entry_rc"
if [ "$fresh_rc" -ne 0 ] || [ "$identity_rc" -ne 0 ] \
   || [ "$copy_rc" -ne 0 ] || [ "$runtime_build_rc" -ne 0 ] \
   || [ "$concrete_rc" -ne 0 ] || [ "$proof_build_rc" -ne 0 ] \
   || [ "$loop_rc" -ne 0 ] || [ "$entry_rc" -ne 0 ]; then
  exit 1
fi
exit 0
