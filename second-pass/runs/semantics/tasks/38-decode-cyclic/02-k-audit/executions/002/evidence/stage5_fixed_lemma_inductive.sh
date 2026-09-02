#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/38-decode-cyclic
log=/audit-output/evidence/stage5_fixed_lemma_inductive.log

{
  cd "$scratch" || exit 1
  echo '$ kprove spec-fixed-slice-lemmas.k --definition fixed-proof-kompiled --spec-module SPEC-FIXED-SLICE-LEMMAS'
  kprove spec-fixed-slice-lemmas.k \
    --definition fixed-proof-kompiled \
    --spec-module SPEC-FIXED-SLICE-LEMMAS
  status=$?
  echo "EXIT_STATUS=$status"
  exit "$status"
} >"$log" 2>&1
