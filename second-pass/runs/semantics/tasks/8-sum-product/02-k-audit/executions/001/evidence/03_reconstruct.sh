#!/usr/bin/env bash
set -u

WORK=/tmp/audit-work/reconstruction
cd "$WORK" || exit 99

run() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf 'EXIT_STATUS: %d\n' "$rc"
  return 0
}

printf 'TOOLCHAIN\n'
run kompile --version
run kprove --version
run krun --version

printf '\nCLEANNESS_BEFORE_BUILD\n'
run find "$WORK" -maxdepth 1 -type d -name '*-kompiled' -print

printf '\nCONCRETE_DEFINITION_AND_EXECUTION\n'
run kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

printf 'COMMAND: python3 %q %q > %q\n' \
  "$WORK/trusted/py2mpy.py" /audit-output/evidence/concrete-audit.py \
  "$WORK/concrete-audit.mpy"
python3 "$WORK/trusted/py2mpy.py" /audit-output/evidence/concrete-audit.py \
  > "$WORK/concrete-audit.mpy"
rc=$?
printf 'EXIT_STATUS: %d\n' "$rc"
run krun concrete-audit.mpy --definition runtime-kompiled --output pretty

printf '\nLOOP_PROOF_DEFINITION_AND_TARGET\n'
run kompile verification.k \
  --backend haskell \
  --main-module SUM-PRODUCT-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
run kprove spec.k \
  --definition verification-kompiled \
  --spec-module SUM-PRODUCT-LOOP-SPEC \
  --output pretty

printf '\nFUNCTION_PROOF_DEFINITION_AND_TARGET\n'
run kompile verification.k \
  --backend haskell \
  --main-module SUM-PRODUCT-LEMMA \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-lemma-kompiled
run kprove spec.k \
  --definition verification-lemma-kompiled \
  --spec-module SUM-PRODUCT-FUNCTION-SPEC \
  --output pretty
