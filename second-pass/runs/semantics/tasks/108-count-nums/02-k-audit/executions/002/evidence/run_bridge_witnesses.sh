#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence
spec=operational-bridge-witness-spec.k
overall=0

run_case() {
  label=$1
  expectation=$2
  definition=$3
  module=$4
  temporary=$(mktemp "/tmp/${label}.XXXXXX")
  command=(kprove "$spec" --definition "$definition" --spec-module "$module")
  printf 'RUN %s expectation=%s\n' "$label" "$expectation"
  printf 'COMMAND:'
  printf ' %q' "${command[@]}"
  printf '\n'
  "${command[@]}" >"$temporary" 2>&1
  status=$?
  lines=$(wc -l <"$temporary")
  {
    printf 'COMMAND:'
    printf ' %q' "${command[@]}"
    printf '\n'
    printf 'EXPECTATION=%s\n' "$expectation"
    printf 'EXIT_STATUS=%s\n' "$status"
    printf 'OUTPUT_LINES=%s\n' "$lines"
    if [ "$lines" -le 260 ]; then
      sed -n '1,260p' "$temporary"
    else
      sed -n '1,130p' "$temporary"
      printf '[... %s lines omitted from bounded log ...]\n' "$((lines - 260))"
      tail -n 130 "$temporary"
    fi
  } >"$evidence/05-${label}.log"
  if [ "$expectation" = "top" ]; then
    if [ "$status" -eq 0 ] && rg -q '^#Top$' "$evidence/05-${label}.log"; then
      printf 'CASE_RESULT %s=PASS(top)\n' "$label"
    else
      printf 'CASE_RESULT %s=FAIL(expected top)\n' "$label"
      overall=1
    fi
  else
    if [ "$status" -ne 0 ] && rg -q 'WarnStuckClaimState' "$evidence/05-${label}.log"; then
      printf 'CASE_RESULT %s=PASS(stuck)\n' "$label"
    else
      printf 'CASE_RESULT %s=FAIL(expected meaningful stuck claim)\n' "$label"
      overall=1
    fi
  fi
  tail -n 8 "$evidence/05-${label}.log"
  rm -f "$temporary"
}

cd "$scratch" || exit 2
cp "$evidence/operational-bridge-witness-spec.k" "$spec"

run_case helper-fixed-stuck stuck audit-digit-loop-kompiled AUDIT-HELPER-BROAD-CONTEXT-SPEC
run_case helper-bridge-fabricates top audit-digit-function-kompiled AUDIT-HELPER-BROAD-CONTEXT-SPEC

run_case signed-fixed-99 top audit-digit-function-kompiled AUDIT-SIGNED-FIXED-RESULT-SPEC
run_case signed-fixed-rejects-minus1 stuck audit-digit-function-kompiled AUDIT-SIGNED-BRIDGE-RESULT-SPEC
run_case signed-bridge-fabricates-minus1 top audit-signed-digit-kompiled AUDIT-SIGNED-BRIDGE-RESULT-SPEC

run_case count-with-n-fixed-1 top audit-signed-digit-kompiled AUDIT-COUNT-WITH-N-FIXED-RESULT-SPEC
run_case count-with-n-fixed-rejects-0 stuck audit-signed-digit-kompiled AUDIT-COUNT-WITH-N-BRIDGE-RESULT-SPEC
run_case count-with-n-bridge-fabricates-0 top audit-count-loop-with-n-kompiled AUDIT-COUNT-WITH-N-BRIDGE-RESULT-SPEC

run_case count-initial-fixed-1 top audit-count-loop-with-n-kompiled AUDIT-COUNT-INITIAL-FIXED-RESULT-SPEC
run_case count-initial-fixed-rejects-0 stuck audit-count-loop-with-n-kompiled AUDIT-COUNT-INITIAL-BRIDGE-RESULT-SPEC
run_case count-initial-bridge-fabricates-0 top audit-count-loop-kompiled AUDIT-COUNT-INITIAL-BRIDGE-RESULT-SPEC

printf 'OPERATIONAL_WITNESS_EXIT_STATUS=%s\n' "$overall"
exit "$overall"
