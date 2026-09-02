#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

cd /tmp/audit-work/proof-audit || exit 97

printf '[toolchain]\n'
run command -v kompile
run command -v krun
run command -v kprove
run kompile --version
run kprove --version

printf '[scratch cleanliness before fresh builds]\n'
run find . -maxdepth 1 -type d -name '*-kompiled' -print

printf '[independent concrete source translation]\n'
run bash -c 'python3 /reference/py2mpy.py /audit-output/evidence/audit_concrete.py > audit_concrete.mpy'
run sha256sum audit_concrete.mpy

printf '[fresh supplied-semantics concrete build]\n'
run kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition concrete-kompiled
run krun audit_concrete.mpy --definition concrete-kompiled

printf '[positive target-claim inventory]\n'
run rg -n '^[[:space:]]*claim([[:space:]]|$)' spec.k

printf '[fresh proof build]\n'
run kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

printf '[all positive target claims: SPEC contains exactly the one inventoried claim]\n'
run kprove spec.k --definition verification-kompiled --spec-module SPEC
