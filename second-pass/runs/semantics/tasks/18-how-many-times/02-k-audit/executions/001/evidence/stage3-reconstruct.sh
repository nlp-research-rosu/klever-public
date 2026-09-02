#!/usr/bin/env bash
set -u
set -x

export PATH="$HOME/.nix-profile/bin:$PATH"
work=/tmp/audit-work/rebuild-final
mkdir -p "$work"
cp /candidate/solution.mpy "$work/solution.mpy"
cp /candidate/spec.k "$work/spec.k"
cp /candidate/verification.k "$work/verification.k"
cp /candidate/concrete-tests.mpy "$work/concrete-tests.mpy"
cp -a /reference/reference-semantics "$work/reference-semantics"

kompile --version
kprove --version
krun --version

kompile "$work/reference-semantics/semantics.k" \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition "$work/runtime-kompiled"
llvm_build_rc=$?
echo "LLVM_BUILD_EXIT=$llvm_build_rc"

if test "$llvm_build_rc" -eq 0; then
  krun "$work/concrete-tests.mpy" \
    --definition "$work/runtime-kompiled"
  concrete_rc=$?
else
  concrete_rc=125
fi
echo "CONCRETE_KRUN_EXIT=$concrete_rc"

kompile "$work/verification.k" \
  --backend haskell \
  --main-module HOW-MANY-TIMES-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$work/verification-kompiled"
haskell_build_rc=$?
echo "HASKELL_BUILD_EXIT=$haskell_build_rc"

if test "$haskell_build_rc" -eq 0; then
  kprove "$work/spec.k" \
    --definition "$work/verification-kompiled" \
    --spec-module HOW-MANY-TIMES-SPEC
  combined_rc=$?

  kprove /audit-output/evidence/spec-labeled.k \
    --definition "$work/verification-kompiled" \
    --spec-module HOW-MANY-TIMES-SPEC-AUDIT \
    --claims HOW-MANY-TIMES-SPEC-AUDIT.overlap-acc
  helper_rc=$?

  kprove /audit-output/evidence/spec-labeled.k \
    --definition "$work/verification-kompiled" \
    --spec-module HOW-MANY-TIMES-SPEC-AUDIT \
    --claims HOW-MANY-TIMES-SPEC-AUDIT.overlap-acc,HOW-MANY-TIMES-SPEC-AUDIT.entry \
    --trusted HOW-MANY-TIMES-SPEC-AUDIT.overlap-acc
  entry_rc=$?
else
  combined_rc=125
  helper_rc=125
  entry_rc=125
fi

echo "COMBINED_KPROVE_EXIT=$combined_rc"
echo "HELPER_KPROVE_EXIT=$helper_rc"
echo "ENTRY_KPROVE_EXIT=$entry_rc"

if test "$llvm_build_rc" -ne 0 ||
   test "$concrete_rc" -ne 0 ||
   test "$haskell_build_rc" -ne 0 ||
   test "$combined_rc" -ne 0 ||
   test "$helper_rc" -ne 0 ||
   test "$entry_rc" -ne 0
then
  exit 1
fi
exit 0
