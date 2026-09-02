#!/usr/bin/env bash
set +e

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

scratch=/tmp/audit-work/102-choose-num
printf 'Stage 3 clean concrete-semantics reconstruction\n'
run kompile --version

printf '\n$ cd %q && python3 trusted/py2mpy.py /audit-output/evidence/concrete_audit.py > concrete_audit.mpy\n' "$scratch"
(
  cd "$scratch" || exit 125
  python3 trusted/py2mpy.py /audit-output/evidence/concrete_audit.py > concrete_audit.mpy
)
status=$?
printf '[exit %d]\n' "$status"

run kompile "$scratch/reference-semantics/semantics.k" \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition "$scratch/runtime-kompiled"

run krun "$scratch/concrete_audit.mpy" \
  --definition "$scratch/runtime-kompiled"
