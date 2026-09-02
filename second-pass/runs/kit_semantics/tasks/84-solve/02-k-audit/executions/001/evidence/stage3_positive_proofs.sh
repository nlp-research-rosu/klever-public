#!/usr/bin/env bash
set -euo pipefail

work=/tmp/audit-work/84-solve
evidence=/audit-output/evidence
raw=/tmp/audit-work/84-solve/raw-logs
mkdir -p "$raw"

run_bounded() {
  local name=$1
  shift
  local raw_log="$raw/$name.raw.log"
  local evidence_log="$evidence/$name.log"
  {
    printf 'COMMAND:'
    printf ' %q' "$@"
    printf '\n'
  } > "$evidence_log"
  set +e
  "$@" > "$raw_log" 2>&1
  local status=$?
  set -e
  {
    printf 'EXIT_STATUS=%s\n' "$status"
    printf 'OUTPUT_LINES=%s\n' "$(wc -l < "$raw_log")"
    sed -n '1,120p' "$raw_log"
    if [[ $(wc -l < "$raw_log") -gt 240 ]]; then
      printf '[... bounded log: middle omitted ...]\n'
      tail -n 120 "$raw_log"
    else
      sed -n '121,240p' "$raw_log"
    fi
  } >> "$evidence_log"
  return "$status"
}

cd "$work"

run_bounded stage3-proof-bridge-suite \
  kprove bridge-spec.k \
    --definition bridge-audit-kompiled \
    --spec-module BRIDGE-SPEC

claims=(
  digit-sum-bound
  solve-sum-00-07
  solve-sum-08-15
  solve-sum-16-23
  solve-sum-24-31
  solve-sum-32-36
)
for claim in "${claims[@]}"; do
  run_bounded "stage3-proof-$claim" \
    kprove spec.k \
      --definition verification-audit-kompiled \
      --spec-module SPEC \
      --claims "SPEC.$claim"
done

run_bounded stage3-proof-target-suite \
  kprove spec.k \
    --definition verification-audit-kompiled \
    --spec-module SPEC
