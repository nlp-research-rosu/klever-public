#!/usr/bin/env bash
set -u

definition=/tmp/audit-work/build/verification-kompiled
spec=/tmp/audit-work/source/spec.k
evidence=/audit-output/evidence/stage3
claims=(
  empty-list
  prompt-example-one
  prompt-example-two
  format-all-counts
  character-loop-base
  even-character-step
  odd-character-step
  list-loop-base
  append-base
  append-step
)

overall=0
for claim in "${claims[@]}"; do
  log="$evidence/kprove-$claim.log"
  {
    printf '$ kprove %q --definition %q --spec-module ODD-COUNT-SPEC --claims %q --output pretty\n' \
      "$spec" "$definition" "ODD-COUNT-SPEC.$claim"
    kprove "$spec" \
      --definition "$definition" \
      --spec-module ODD-COUNT-SPEC \
      --claims "ODD-COUNT-SPEC.$claim" \
      --output pretty
    status=$?
    echo "exit: $status"
    if [[ $status -ne 0 ]]; then
      exit "$status"
    fi
  } >"$log" 2>&1
  status=$?
  if [[ $status -ne 0 ]] || ! grep -Fxq '#Top' "$log"; then
    overall=1
  fi
done

{
  echo "claims attempted: ${#claims[@]}"
  for claim in "${claims[@]}"; do
    log="$evidence/kprove-$claim.log"
    status_line=$(tail -n 1 "$log")
    top_count=$(grep -Fxc '#Top' "$log" || true)
    echo "$claim: $status_line; #Top lines: $top_count"
  done
  echo "overall exit: $overall"
} >"$evidence/kprove-positive-summary.log"

exit "$overall"
