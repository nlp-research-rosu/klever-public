#!/usr/bin/env bash
set -u

submitted=$(tr -d '[:space:]' < solution.mpy)
macro_rhs=$(
  sed -n '/^[[:space:]]*rule solutionProgram =>/,$p' verification.k |
    sed '1d;$d' |
    tr -d '[:space:]'
)

printf 'SUBMITTED_NORMALIZED_SHA256: '
printf '%s' "$submitted" | sha256sum | awk '{print $1}'
printf 'MACRO_RHS_NORMALIZED_SHA256: '
printf '%s' "$macro_rhs" | sha256sum | awk '{print $1}'

if [[ "$submitted" == "$macro_rhs" ]]; then
  printf '%s\n' 'NORMALIZED_TREE_IDENTITY: YES'
  exit 0
fi

printf '%s\n' 'NORMALIZED_TREE_IDENTITY: NO'
printf 'SUBMITTED: %s\n' "$submitted"
printf 'MACRO_RHS: %s\n' "$macro_rhs"
exit 1
