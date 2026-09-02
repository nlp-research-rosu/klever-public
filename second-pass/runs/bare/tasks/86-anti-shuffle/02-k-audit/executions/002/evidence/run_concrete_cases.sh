#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/anti-shuffle
definition="$work/audit-semantics-kompiled"
program="$work/solution.mpy"

labels=(
  empty
  one-space
  example-hi
  example-hello
  example-prompt
  repeated-edge-spaces
  insert-greater
  insert-less
  punctuation
  unicode
)
k_inputs=(
  '""'
  '" "'
  '"Hi"'
  '"hello"'
  '"Hello World!!!"'
  '"  ba  dc "'
  '"ab"'
  '"ba"'
  '"z9! A0?"'
  '"éA Ωβ"'
)

status=0
for index in "${!labels[@]}"; do
  label=${labels[$index]}
  input=${k_inputs[$index]}
  printf 'CASE: %s\n' "$label"
  printf 'COMMAND: krun %q --definition %q -cINPUT=%q\n' \
    "$program" "$definition" "$input"
  krun "$program" --definition "$definition" -cINPUT="$input"
  current=$?
  printf 'CASE_EXIT_STATUS: %d\n' "$current"
  if [[ "$current" -ne 0 ]]; then
    status=$current
  fi
done
exit "$status"
