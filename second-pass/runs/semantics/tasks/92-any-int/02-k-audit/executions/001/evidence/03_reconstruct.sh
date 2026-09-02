#!/usr/bin/env bash
set -u

source_dir=/candidate
work=/tmp/audit-work/reconstruction

echo '$ create a source-only reconstruction tree under /tmp/audit-work'
if test -e "$work"; then
  echo "refusing to reuse existing reconstruction directory: $work"
  exit 90
fi
mkdir -p "$work"
cp -a "$source_dir/reference-semantics" "$work/reference-semantics"
cp "$source_dir/solution.py" "$source_dir/solution.mpy" \
   "$source_dir/concrete_tests.py" "$source_dir/spec.k" \
   "$source_dir/verification.k" "$work/"
copy_status=$?
echo "exit=$copy_status"
find "$work" -type d \( -name '*-kompiled' -o -name __pycache__ \) -print
find "$work" -type f \( -name '*.pyc' -o -name '*.cache' \) -print

echo '$ python3 /reference/py2mpy.py concrete_tests.py > audit-concrete-tests.mpy'
python3 /reference/py2mpy.py "$work/concrete_tests.py" > "$work/audit-concrete-tests.mpy"
translate_status=$?
echo "exit=$translate_status"

echo '$ kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled'
(
  cd "$work" &&
  kompile reference-semantics/semantics.k \
    --backend llvm \
    --main-module MPY-KRUN \
    --syntax-module MPY-SYNTAX \
    --output-definition runtime-kompiled
)
llvm_build_status=$?
echo "exit=$llvm_build_status"

if test "$llvm_build_status" -eq 0; then
  echo '$ krun audit-concrete-tests.mpy --definition runtime-kompiled'
  (
    cd "$work" &&
    krun audit-concrete-tests.mpy --definition runtime-kompiled
  )
  concrete_status=$?
  echo "exit=$concrete_status"
else
  concrete_status=125
  echo "SKIPPED krun because LLVM build failed"
fi

echo '$ kompile verification.k --backend haskell --main-module ANY-INT-VERIFICATION --syntax-module ANY-INT-VERIFICATION --output-definition verification-kompiled'
(
  cd "$work" &&
  kompile verification.k \
    --backend haskell \
    --main-module ANY-INT-VERIFICATION \
    --syntax-module ANY-INT-VERIFICATION \
    --output-definition verification-kompiled
)
haskell_build_status=$?
echo "exit=$haskell_build_status"

if test "$haskell_build_status" -eq 0; then
  echo '$ kprove spec.k --definition verification-kompiled --spec-module ANY-INT-SPEC'
  (
    cd "$work" &&
    kprove spec.k \
      --definition verification-kompiled \
      --spec-module ANY-INT-SPEC
  )
  all_claims_status=$?
  echo "exit=$all_claims_status"
else
  all_claims_status=125
  echo "SKIPPED kprove because Haskell build failed"
fi

printf 'SUMMARY copy=%s translate=%s llvm_build=%s concrete=%s haskell_build=%s all_claims=%s\n' \
  "$copy_status" "$translate_status" "$llvm_build_status" "$concrete_status" \
  "$haskell_build_status" "$all_claims_status"

if test "$copy_status" -eq 0 &&
   test "$translate_status" -eq 0 &&
   test "$llvm_build_status" -eq 0 &&
   test "$concrete_status" -eq 0 &&
   test "$haskell_build_status" -eq 0 &&
   test "$all_claims_status" -eq 0
then
  exit 0
fi
exit 1
