#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/76-is-simple-power
definition="$scratch/fresh-verification-kompiled"
spec="$scratch/spec.k"

claims=(
  SPEC.emitted-tree-is-shared-tree
  SPEC.returns-on-one
  SPEC.rejects-below-one
  SPEC.rejects-small-base
  SPEC.active-path-enters-loop
  SPEC.loop-correct
)

overall=0
for claim in "${claims[@]}"; do
  printf '$ kprove %s --definition %s --claims %s\n' "$spec" "$definition" "$claim"
  kprove "$spec" --definition "$definition" --claims "$claim"
  status=$?
  printf 'EXIT[%s]=%d\n' "$claim" "$status"
  if [[ "$status" -ne 0 ]]; then
    overall=1
  fi
done

exit "$overall"
