#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/132-is-nested/source
evidence=/audit-output/evidence

run_logged() {
  local name=$1
  shift
  local raw="$scratch/${name}.raw.log"
  local bounded="$evidence/${name}.log"
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@" >"$raw" 2>&1
  local command_status=$?
  {
    printf '$'
    printf ' %q' "$@"
    printf '\n[exit %d]\n' "$command_status"
    printf '%s\n' '[bounded output: last 240 lines]'
    tail -n 240 "$raw"
  } >"$bounded"
  printf '[exit %d; bounded log %s]\n' "$command_status" "$bounded"
  tail -n 20 "$raw"
  return 0
}

cd "$scratch" || exit 99

run_logged stage3_scan_loop \
  timeout 600s kprove \
    --definition verification-kompiled \
    --spec-module IS-NESTED-LOOP-SPEC \
    --claims IS-NESTED-LOOP-SPEC.scan-loop \
    spec.k

run_logged stage3_empty_input \
  timeout 600s kprove \
    --definition verification-with-lemma-kompiled \
    --spec-module IS-NESTED-TOP-SPEC \
    --claims IS-NESTED-TOP-SPEC.empty-input \
    spec.k

run_logged stage3_all_bracket_strings \
  timeout 600s kprove \
    --definition verification-with-lemma-kompiled \
    --spec-module IS-NESTED-TOP-SPEC \
    --claims IS-NESTED-TOP-SPEC.all-bracket-strings \
    spec.k
