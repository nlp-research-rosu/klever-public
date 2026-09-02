#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/38-decode-cyclic
log=/audit-output/evidence/stage5_fixed_lemma_check.log

{
  cd "$scratch" || exit 1

  echo '$ kompile reference-semantics/semantics.k --backend haskell --main-module MPY --syntax-module MPY-SYNTAX --output-definition fixed-proof-kompiled'
  kompile reference-semantics/semantics.k \
    --backend haskell \
    --main-module MPY \
    --syntax-module MPY-SYNTAX \
    --output-definition fixed-proof-kompiled
  build_status=$?
  echo "EXIT_STATUS=$build_status"
  (( build_status == 0 )) || exit 1

  echo
  echo '$ kprove spec-fixed-slice-lemmas.k --definition fixed-proof-kompiled --spec-module SPEC-FIXED-SLICE-LEMMAS'
  kprove spec-fixed-slice-lemmas.k \
    --definition fixed-proof-kompiled \
    --spec-module SPEC-FIXED-SLICE-LEMMAS
  prove_status=$?
  echo "EXIT_STATUS=$prove_status"
  exit "$prove_status"
} >"$log" 2>&1
