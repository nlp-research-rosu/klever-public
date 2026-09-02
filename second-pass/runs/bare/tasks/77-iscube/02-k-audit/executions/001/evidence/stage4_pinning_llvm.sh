#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/77-iscube
src="$scratch/candidate-src"
definition="$scratch/audit-verification-llvm-kompiled"

printf '$ test ! -e %q\n' "$definition"
test ! -e "$definition"
printf '[exit %d]\n' "$?"

printf '\n$ kompile %q --main-module VERIFICATION --syntax-module VERIFICATION --backend llvm --output-definition %q\n' \
  "$src/verification.k" "$definition"
kompile "$src/verification.k" \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --backend llvm \
  --output-definition "$definition"
build_status=$?
printf '[exit %d]\n' "$build_status"

if (( build_status != 0 )); then
  exit "$build_status"
fi

for input in 8 -8 9 -9; do
  expected=true
  if [[ "$input" == 9 || "$input" == -9 ]]; then
    expected=false
  fi
  printf '\n$ krun %q -cN=%q --definition %q\n' \
    "$scratch/iscubeProgram.pgm" "$input" "$definition"
  output="$(krun "$scratch/iscubeProgram.pgm" -cN="$input" --definition "$definition" 2>&1)"
  status=$?
  printf '%s\n' "$output"
  printf '[exit %d]\n' "$status"
  if (( status == 0 )) \
    && grep -Eq "BoolVal[[:space:]]*\\([[:space:]]*$expected[[:space:]]*\\)" <<<"$output"; then
    printf 'PINNING input=%s expected=%s status=MATCH\n' "$input" "$expected"
  else
    printf 'PINNING input=%s expected=%s status=MISMATCH\n' "$input" "$expected"
    exit 1
  fi
done
