#!/usr/bin/env bash
set -uo pipefail

if [[ $# -ne 3 ]]; then
  echo "usage: $0 SPEC.k DEFINITION OUTPUT_DIR" >&2
  exit 64
fi

spec=$1
definition=$2
output_dir=$3
mkdir -p "$output_dir"

claims=(
  longest-loop
  longest-empty
  longest-nonempty
  concrete-empty
  concrete-first-tie
  concrete-increasing
  concrete-late-tie
)

failures=0
for claim in "${claims[@]}"; do
  log="$output_dir/$claim.log"
  claim_filter="SPEC.$claim"
  # The nonempty entry theorem uses longest-loop as its circularity. Keep only
  # that exact helper alongside the independently selected entry target.
  if [[ "$claim" == "longest-nonempty" ]]; then
    claim_filter="SPEC.longest-loop,SPEC.longest-nonempty"
  fi
  command=(
    kprove "$spec"
    --definition "$definition"
    --spec-module SPEC
    --claims "$claim_filter"
    --output pretty
    --warnings none
    --haskell-backend-command "kore-exec --log-level error"
  )
  {
    printf 'COMMAND:'
    printf ' %q' "${command[@]}"
    printf '\nWORKDIR: %s\n--- OUTPUT ---\n' "$PWD"
  } >"$log"
  "${command[@]}" >>"$log" 2>&1
  status=$?
  {
    printf '%s\n' '--- END OUTPUT ---'
    printf 'EXIT_STATUS: %d\n' "$status"
  } >>"$log"
  top_count=$(grep -c '^#Top$' "$log" || true)
  printf 'CLAIM %s EXIT_STATUS %d TOP_COUNT %d LOG %s\n' \
    "$claim" "$status" "$top_count" "$log"
  if [[ $status -ne 0 || $top_count -ne 1 ]]; then
    failures=$((failures + 1))
  fi
done

printf 'claims=%d\n' "${#claims[@]}"
printf 'failures=%d\n' "$failures"
exit "$failures"
