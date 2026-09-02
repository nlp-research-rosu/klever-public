#!/usr/bin/env bash
set -u

overall=0
run() {
  echo "\$ $*"
  "$@"
  status=$?
  echo "EXIT: $status"
  if [ "$status" -ne 0 ]; then
    overall=1
  fi
  return 0
}

run command -v kompile
run command -v krun
run command -v kprove
run kompile --version
run kprove --version

cd /tmp/audit-work/fresh || exit 125
echo '$ python3 py2mpy.py concrete_tests.py > concrete_tests.regenerated.mpy'
python3 py2mpy.py concrete_tests.py > concrete_tests.regenerated.mpy
status=$?
echo "EXIT: $status"
if [ "$status" -ne 0 ]; then overall=1; fi
run cmp concrete_tests.mpy concrete_tests.regenerated.mpy

run kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
run krun concrete_tests.regenerated.mpy \
  --definition audit-runtime-kompiled

run kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-base-kompiled
run kprove spec.k \
  --definition audit-verification-base-kompiled \
  --spec-module SPEC-LEMMA \
  --output pretty

run kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
run kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC \
  --output pretty

echo "STAGE3_OVERALL_EXIT: $overall"
exit "$overall"
