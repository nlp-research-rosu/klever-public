#!/usr/bin/env bash
set -uo pipefail

work_root=$(mktemp -d /tmp/audit-work/stage1-recheck.XXXXXX)
echo "fresh_work_root=$work_root"

echo '$ cp -a /reference/k-proof/. "$work_root"/'
cp -a /reference/k-proof/. "$work_root"/
copy_rc=$?
echo "exit_code=$copy_rc"
if [ "$copy_rc" -ne 0 ]; then
  exit "$copy_rc"
fi

cd "$work_root" || exit 1

echo '$ kompile verification.k --backend haskell --main-module FACTORIZE-VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled'
kompile verification.k \
  --backend haskell \
  --main-module FACTORIZE-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
base_compile_rc=$?
echo "exit_code=$base_compile_rc"
if [ "$base_compile_rc" -ne 0 ]; then
  exit "$base_compile_rc"
fi

echo '$ kprove spec.k --definition verification-kompiled --spec-module FACTORIZE-LOOP-SPEC --output pretty'
kprove spec.k \
  --definition verification-kompiled \
  --spec-module FACTORIZE-LOOP-SPEC \
  --output pretty
loop_proof_rc=$?
echo "exit_code=$loop_proof_rc"
if [ "$loop_proof_rc" -ne 0 ]; then
  exit "$loop_proof_rc"
fi

echo '$ kompile verification.k --backend haskell --main-module FACTORIZE-VERIFICATION-WITH-LOOP-LEMMA --syntax-module MPY-SYNTAX --output-definition verification-with-lemma-kompiled'
kompile verification.k \
  --backend haskell \
  --main-module FACTORIZE-VERIFICATION-WITH-LOOP-LEMMA \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-with-lemma-kompiled
lemma_compile_rc=$?
echo "exit_code=$lemma_compile_rc"
if [ "$lemma_compile_rc" -ne 0 ]; then
  exit "$lemma_compile_rc"
fi

echo '$ kprove spec.k --definition verification-with-lemma-kompiled --spec-module FACTORIZE-SPEC --output pretty'
kprove spec.k \
  --definition verification-with-lemma-kompiled \
  --spec-module FACTORIZE-SPEC \
  --output pretty
entry_proof_rc=$?
echo "exit_code=$entry_proof_rc"
exit "$entry_proof_rc"
