#!/usr/bin/env bash
set -u

run() {
  label=$1
  shift
  printf '\nLABEL: %s\nCOMMAND:' "$label"
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %s\n' "$status"
  return "$status"
}

overall=0

run concrete_kompile \
  kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled || overall=1

run concrete_translate \
  python3 py2mpy.py /audit-output/evidence/concrete_semantics_tests.py || overall=1

# Translation output is captured separately to avoid conflating it with logs.
python3 py2mpy.py /audit-output/evidence/concrete_semantics_tests.py \
  > audit-concrete-tests.mpy
translate_capture_status=$?
printf '\nLABEL: concrete_translate_capture\nCOMMAND: python3 py2mpy.py /audit-output/evidence/concrete_semantics_tests.py > audit-concrete-tests.mpy\n'
printf 'EXIT_STATUS: %s\n' "$translate_capture_status"
if (( translate_capture_status != 0 )); then overall=1; fi

run concrete_krun \
  krun audit-concrete-tests.mpy \
  --definition audit-runtime-kompiled \
  --output pretty || overall=1

run proof_kompile \
  kompile verification.k \
  --backend haskell \
  --main-module SUM-SQUARES-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled || overall=1

run prove_loop \
  kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SUM-SQUARES-SPEC \
  --claims SUM-SQUARES-SPEC.loop \
  --output pretty || overall=1

run prove_body \
  kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SUM-SQUARES-SPEC \
  --claims SUM-SQUARES-SPEC.body,SUM-SQUARES-SPEC.loop \
  --trusted SUM-SQUARES-SPEC.loop \
  --output pretty || overall=1

run prove_main \
  kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SUM-SQUARES-SPEC \
  --claims SUM-SQUARES-SPEC.main,SUM-SQUARES-SPEC.body \
  --trusted SUM-SQUARES-SPEC.body \
  --output pretty || overall=1

printf '\nOVERALL_EXIT_STATUS: %s\n' "$overall"
exit "$overall"
