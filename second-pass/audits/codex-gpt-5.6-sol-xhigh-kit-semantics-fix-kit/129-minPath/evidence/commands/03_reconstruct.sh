#!/usr/bin/env bash
set +e

overall=0
run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  if [ "$status" -ne 0 ]; then overall=1; fi
}

cd /tmp/audit-work/129-minpath || exit 99

run kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-fresh-kompiled

printf '\n$ python3 /reference/py2mpy.py /audit-output/evidence/artifacts/concrete_probe.py > concrete-probe.mpy\n'
python3 /reference/py2mpy.py /audit-output/evidence/artifacts/concrete_probe.py > concrete-probe.mpy
status=$?
printf '[exit %d]\n' "$status"
if [ "$status" -ne 0 ]; then overall=1; fi

run krun concrete-probe.mpy --definition runtime-fresh-kompiled

run kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-fresh-kompiled

printf '\n$ kast --definition verification-fresh-kompiled --sort Module solution.regenerated.mpy > solution.kast\n'
kast --definition verification-fresh-kompiled --sort Module solution.regenerated.mpy > solution.kast
status=$?
printf '[exit %d]\n' "$status"
if [ "$status" -ne 0 ]; then overall=1; fi

printf '\n$ kast --definition verification-fresh-kompiled --module VERIFICATION --sort Module --expand-macros /audit-output/evidence/artifacts/MINPATH-PROGRAM.mpy > macro.kast\n'
kast --definition verification-fresh-kompiled --module VERIFICATION --sort Module --expand-macros /audit-output/evidence/artifacts/MINPATH-PROGRAM.mpy > macro.kast
status=$?
printf '[exit %d]\n' "$status"
if [ "$status" -ne 0 ]; then overall=1; fi

run cmp solution.kast macro.kast
run sha256sum solution.kast macro.kast

run kprove spec.k --definition verification-fresh-kompiled \
  --spec-module SPEC --claims SPEC.answer-loop
run kprove spec.k --definition verification-fresh-kompiled \
  --spec-module SPEC --claims SPEC.all-valid-2x2-k3
run kprove spec.k --definition verification-fresh-kompiled \
  --spec-module SPEC --claims SPEC.example-one
run kprove spec.k --definition verification-fresh-kompiled \
  --spec-module SPEC --claims SPEC.example-two

exit "$overall"
