#!/usr/bin/env bash
set -u

cd /tmp/audit-work/reconstruction || exit 90
overall=0

run() {
  echo "COMMAND: $*"
  "$@"
  local rc=$?
  echo "EXIT_STATUS: $rc"
  if [[ "$rc" -ne 0 ]]; then
    overall=1
  fi
  return 0
}

echo "SOURCE_DEFINITION_CHECK"
find . -maxdepth 2 -printf '%y %P -> %l\n' | LC_ALL=C sort
if find . -type l -print -quit | grep -q .; then
  echo "UNEXPECTED_SCRATCH_SYMLINK"
  overall=1
fi

echo "COMMAND: python3 py2mpy.py smoke.py > smoke.mpy"
python3 py2mpy.py smoke.py > smoke.mpy
translation_rc=$?
echo "EXIT_STATUS: $translation_rc"
if [[ "$translation_rc" -ne 0 ]]; then
  overall=1
fi

run kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-runtime-kompiled
run krun smoke.mpy --definition fresh-runtime-kompiled

run kompile --backend haskell connection-verification.k \
  --main-module CONNECTION-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-connection-kompiled
run kprove connection-spec.k \
  --definition fresh-connection-kompiled \
  --spec-module CONNECTION-SPEC

run kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-verification-kompiled
run kprove spec.k \
  --definition fresh-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.inner-loop
run kprove spec.k \
  --definition fresh-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.inner-loop,SPEC.outer-loop
run kprove spec.k \
  --definition fresh-verification-kompiled \
  --spec-module SPEC

echo "SCRIPT_EXIT=$overall"
exit "$overall"
