#!/usr/bin/env bash
set -u

cd /tmp/audit-work/review/candidate-src
printf 'PWD=%s\n' "$PWD"
printf '%s\n' \
  'COMMAND: kompile --backend haskell reference-semantics/semantics.k --main-module MPY --syntax-module MPY-SYNTAX --output-definition audit-lemma-kompiled'
kompile --backend haskell reference-semantics/semantics.k \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-lemma-kompiled
build_status=$?
printf 'KOMPILE_BRIDGE_FREE_EXIT=%s\n' "$build_status"
if [ "$build_status" -ne 0 ]; then
  exit "$build_status"
fi

printf '%s\n' \
  'COMMAND: kprove slice-lemma-spec.k --definition audit-lemma-kompiled --spec-module SLICE-LEMMA-SPEC'
kprove slice-lemma-spec.k \
  --definition audit-lemma-kompiled \
  --spec-module SLICE-LEMMA-SPEC
proof_status=$?
printf 'KPROVE_BRIDGE_FREE_SLICE_EXIT=%s\n' "$proof_status"
exit "$proof_status"
