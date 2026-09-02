#!/usr/bin/env bash
set -u

work=/tmp/audit-work/recon
raw_dir="$work/raw-logs"
mkdir -p "$raw_dir"
failed=0

run_bounded() {
  local label=$1
  shift
  local raw="$raw_dir/$label.log"
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@" >"$raw" 2>&1
  local status=$?
  local lines
  lines=$(wc -l <"$raw")
  printf '[captured %d lines in %s]\n' "$lines" "$raw"
  sed -n '1,180p' "$raw"
  if (( lines > 260 )); then
    printf '[... middle omitted from bounded evidence log ...]\n'
    tail -n 80 "$raw"
  fi
  printf '[exit %d]\n' "$status"
  return "$status"
}

run_bounded kast_solution \
  kast solution.mpy \
  --definition runtime-kompiled \
  --sort Module \
  --module MPY-SYNTAX \
  --output json \
  --output-file solution.kast.json || failed=1
run_bounded kast_macro \
  kast \
  --expression 'strangeBody()' \
  --definition verification-base-kompiled \
  --sort Stmts \
  --module VERIFICATION-BASE \
  --expand-macros \
  --output json \
  --output-file body.kast.json || failed=1
run_bounded compare_body python3 /audit-output/evidence/compare_kast_body.py || failed=1

run_bounded ground_base \
  kprove ground-spec.k \
  --definition verification-base-kompiled \
  --spec-module GROUND-SPEC || failed=1
run_bounded ground_summary \
  kprove ground-spec.k \
  --definition verification-kompiled \
  --spec-module GROUND-SPEC
ground_summary_status=$?
if (( ground_summary_status == 0 )); then
  printf 'summary unexpectedly discharged the concrete strengthening\n'
else
  printf 'expected opaque-result residual observed for concrete strengthening\n'
fi

run_bounded continuation_base \
  kprove ground-spec.k \
  --definition verification-base-kompiled \
  --spec-module BRIDGE-CONTINUATION-SPEC || failed=1
run_bounded continuation_summary \
  kprove ground-spec.k \
  --definition verification-kompiled \
  --spec-module BRIDGE-CONTINUATION-SPEC
continuation_summary_status=$?
if (( continuation_summary_status == 0 )); then
  printf 'summary discharged the concrete continuation claim\n'
else
  printf 'summary residual retained the continuation effect but not concrete result equality\n'
fi

printf '\nExpected diagnostic: the over-broad bridge claim must fail without the bridge.\n'
run_bounded overbreadth_base \
  kprove ground-spec.k \
  --definition verification-base-kompiled \
  --spec-module BRIDGE-OVERBREADTH-SPEC \
  --depth 30
overbreadth_base_status=$?
if (( overbreadth_base_status == 0 )); then
  printf 'UNEXPECTED: fixed semantics proved the missing-builtins claim\n'
  failed=1
else
  printf 'expected fixed-semantics rejection observed\n'
fi

printf '\nExpected diagnostic: the same claim closes with the candidate summary.\n'
run_bounded overbreadth_summary \
  kprove ground-spec.k \
  --definition verification-kompiled \
  --spec-module BRIDGE-OVERBREADTH-SPEC
overbreadth_summary_status=$?
if (( overbreadth_summary_status != 0 )); then
  printf 'UNEXPECTED: bridge-enabled proof did not close\n'
  failed=1
else
  printf 'bridge over-breadth witness confirmed\n'
fi

exit "$failed"
