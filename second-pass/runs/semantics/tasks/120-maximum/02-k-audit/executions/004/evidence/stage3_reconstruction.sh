#!/usr/bin/env bash
set -uo pipefail

WORK=/tmp/audit-work/maximum-120-audit
status=0
run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  if (( rc != 0 )); then status=1; fi
}

printf 'Tool versions:\n'
run kompile --version
run kprove --version

printf '\nFresh state (no candidate-built definitions/caches copied):\n'
run find "$WORK" -maxdepth 1 -printf '%f\n'

printf '\nTranslate auditor-authored concrete program with trusted translator:\n'
printf '\n$ (cd %s && python3 py2mpy.py auditor-concrete.py > auditor-concrete.mpy)\n' "$WORK"
(cd "$WORK" && python3 py2mpy.py auditor-concrete.py > auditor-concrete.mpy)
rc=$?
printf '[exit %d]\n' "$rc"
if (( rc != 0 )); then status=1; fi
run sha256sum "$WORK/auditor-concrete.py" "$WORK/auditor-concrete.mpy"

printf '\nFresh concrete definition and execution:\n'
run kompile "$WORK/reference-semantics/semantics.k" \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition "$WORK/runtime-kompiled"
run krun "$WORK/auditor-concrete.mpy" --definition "$WORK/runtime-kompiled"

printf '\nFresh proof definition:\n'
run kompile "$WORK/verification.k" \
  --backend haskell \
  --main-module MAXIMUM-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$WORK/verification-kompiled"

printf '\nOriginal aggregate positive target:\n'
run kprove "$WORK/spec.k" \
  --definition "$WORK/verification-kompiled" \
  --spec-module MAXIMUM-SPEC

printf '\nIndependent k=0 target:\n'
run kprove "$WORK/spec-zero.k" \
  --definition "$WORK/verification-kompiled" \
  --spec-module MAXIMUM-SPEC-ZERO

printf '\nIndependent 0<k<=len target:\n'
run kprove "$WORK/spec-positive.k" \
  --definition "$WORK/verification-kompiled" \
  --spec-module MAXIMUM-SPEC-POSITIVE

exit "$status"
