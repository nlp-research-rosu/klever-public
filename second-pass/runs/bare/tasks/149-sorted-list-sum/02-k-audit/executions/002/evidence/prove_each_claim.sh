#!/usr/bin/env bash
set -euo pipefail

scratch=/tmp/audit-work/reconstruction
definition="$scratch/proof-kompiled"
claims=(
  universal-correctness
  base
  symbolic-two
  symbolic-two-reverse
  symbolic-three
  prompt-example-one
  prompt-example-two
)

for claim in "${claims[@]}"; do
  output="$scratch/reviewer-kprove-${claim}.out"
  printf 'CLAIM %s\n' "$claim"
  (
    cd "$scratch"
    kprove spec.k \
      --definition "$definition" \
      --spec-module SPEC \
      --claims "$claim" \
      --output pretty \
      -w none
  ) > "$output" 2>&1
  status=$?
  sed -n '1,80p' "$output"
  printf 'EXIT %d\n' "$status"
  grep -Fxq '#Top' "$output"
  printf 'TOP true\n'
done

printf 'ALL_POSITIVE_CLAIMS_TOP count=%d\n' "${#claims[@]}"
