#!/usr/bin/env bash
set -u

log=/audit-output/evidence/03_reconstruct.log
exec > >(tee "$log") 2>&1

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  if test "$status" -ne 0; then
    exit "$status"
  fi
}

work=/tmp/audit-work/rebuild/candidate
cd "$work" || exit 1

printf '$ python3 ../trusted/py2mpy.py audit-concrete.py > audit-concrete.mpy\n'
python3 ../trusted/py2mpy.py audit-concrete.py > audit-concrete.mpy
status=$?
printf '[exit %d]\n' "$status"
if test "$status" -ne 0; then
  exit "$status"
fi

run kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

run krun solution.mpy --definition runtime-kompiled
run krun audit-concrete.mpy --definition runtime-kompiled

run kompile verification.k \
  --backend haskell \
  --main-module MPY-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-base-kompiled

run kprove spec.k \
  --definition verification-base-kompiled \
  --spec-module AUX-SPEC

run kompile verification.k \
  --backend haskell \
  --main-module MPY-VERIFICATION-LEMMA \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-lemma-kompiled

run kprove spec.k \
  --definition verification-lemma-kompiled \
  --spec-module MAIN-SPEC
