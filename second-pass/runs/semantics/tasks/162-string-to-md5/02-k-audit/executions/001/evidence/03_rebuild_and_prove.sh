#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/proof-162

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

cd "$scratch" || exit 2

run test ! -e runtime-kompiled
run test ! -e verification-kompiled

run kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

run kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

run kprove spec-empty.k \
  --definition verification-kompiled \
  --spec-module SPEC-EMPTY

run kprove spec-nonempty.k \
  --definition verification-kompiled \
  --spec-module SPEC-NONEMPTY

run kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

printf '$ python3 py2mpy.py audit-empty.py > audit-empty.mpy\n'
python3 py2mpy.py audit-empty.py > audit-empty.mpy
printf '[exit %d]\n' "$?"

printf '$ python3 py2mpy.py audit-example.py > audit-example.mpy\n'
python3 py2mpy.py audit-example.py > audit-example.mpy
printf '[exit %d]\n' "$?"

run krun audit-empty.mpy --definition runtime-kompiled
run krun audit-example.mpy --definition runtime-kompiled --depth 60
