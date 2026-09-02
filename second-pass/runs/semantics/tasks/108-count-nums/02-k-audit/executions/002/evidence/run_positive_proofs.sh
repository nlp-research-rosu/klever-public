#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence
overall=0

run_bounded() {
  label=$1
  shift
  temporary=$(mktemp "/tmp/${label}.XXXXXX")
  printf 'RUN %s\n' "$label"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@" >"$temporary" 2>&1
  status=$?
  lines=$(wc -l <"$temporary")
  {
    printf 'COMMAND:'
    printf ' %q' "$@"
    printf '\n'
    printf 'EXIT_STATUS=%s\n' "$status"
    printf 'OUTPUT_LINES=%s\n' "$lines"
    if [ "$lines" -le 240 ]; then
      sed -n '1,240p' "$temporary"
    else
      sed -n '1,120p' "$temporary"
      printf '[... %s lines omitted from bounded log ...]\n' "$((lines - 240))"
      tail -n 120 "$temporary"
    fi
  } >"$evidence/03-${label}.log"
  tail -n 12 "$evidence/03-${label}.log"
  if [ "$status" -ne 0 ]; then
    overall=1
  fi
  rm -f "$temporary"
  return "$status"
}

check_proof() {
  label=$1
  shift
  run_bounded "$label" "$@"
  status=$?
  if [ "$status" -eq 0 ] && rg -q '^#Top$' "$evidence/03-${label}.log"; then
    printf 'PROOF_RESULT %s exit=0 top=true\n' "$label"
  else
    printf 'PROOF_RESULT %s exit=%s top=false\n' "$label" "$status"
    overall=1
  fi
}

cd "$scratch" || exit 2

run_bounded build-runtime \
  kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
if [ "$?" -eq 0 ]; then
  python3 py2mpy.py concrete_tests.py > audit-concrete-tests.mpy
  cmp audit-concrete-tests.mpy concrete_tests.mpy
  translation_status=$?
  printf 'CONCRETE_TEST_TRANSLATION_CMP_EXIT=%s\n' "$translation_status"
  if [ "$translation_status" -ne 0 ]; then overall=1; fi
  run_bounded concrete-krun \
    krun audit-concrete-tests.mpy --definition audit-runtime-kompiled
fi

run_bounded build-loop-base \
  kompile verification.k \
  --backend haskell \
  --main-module COUNT-NUMS-VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-loop-base-kompiled
if [ "$?" -eq 0 ]; then
  check_proof positive-loop \
    kprove spec.k --definition audit-loop-base-kompiled --spec-module POSITIVE-LOOP-SPEC
  check_proof negative-loop \
    kprove spec.k --definition audit-loop-base-kompiled --spec-module NEGATIVE-LOOP-SPEC
fi

run_bounded build-digit-loop \
  kompile verification.k \
  --backend haskell \
  --main-module DIGIT-LOOP-LEMMAS \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-digit-loop-kompiled
if [ "$?" -eq 0 ]; then
  check_proof positive-function \
    kprove spec.k --definition audit-digit-loop-kompiled --spec-module POSITIVE-FUNCTION-SPEC
  check_proof negative-function \
    kprove spec.k --definition audit-digit-loop-kompiled --spec-module NEGATIVE-FUNCTION-SPEC
fi

run_bounded build-digit-function \
  kompile verification.k \
  --backend haskell \
  --main-module DIGIT-FUNCTION-LEMMAS \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-digit-function-kompiled
if [ "$?" -eq 0 ]; then
  check_proof signed-function \
    kprove spec.k --definition audit-digit-function-kompiled --spec-module SIGNED-FUNCTION-SPEC
fi

run_bounded build-signed-digit \
  kompile verification.k \
  --backend haskell \
  --main-module SIGNED-DIGIT-LEMMA \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-signed-digit-kompiled
if [ "$?" -eq 0 ]; then
  check_proof count-loop-with-n \
    kprove spec.k --definition audit-signed-digit-kompiled --spec-module COUNT-LOOP-WITH-N-SPEC
fi

run_bounded build-count-loop-with-n \
  kompile verification.k \
  --backend haskell \
  --main-module COUNT-LOOP-WITH-N-LEMMA \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-count-loop-with-n-kompiled
if [ "$?" -eq 0 ]; then
  check_proof count-loop \
    kprove spec.k --definition audit-count-loop-with-n-kompiled --spec-module COUNT-LOOP-SPEC
fi

run_bounded build-count-loop \
  kompile verification.k \
  --backend haskell \
  --main-module COUNT-LOOP-LEMMA \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-count-loop-kompiled
if [ "$?" -eq 0 ]; then
  check_proof count-nums \
    kprove spec.k --definition audit-count-loop-kompiled --spec-module COUNT-NUMS-SPEC
fi

printf 'POSITIVE_RECONSTRUCTION_EXIT_STATUS=%s\n' "$overall"
exit "$overall"
