#!/usr/bin/env bash
set -u
set -o pipefail
PS4='+ ${BASH_SOURCE}:${LINENO}: '
set -x

inputs=(1 3 9 10 12 99 100 101 109 110 111 999 1000)

for n in "${inputs[@]}"; do
  python_values=$(
    python3 - "$n" <<'PY'
import sys
from canonical import even_odd_palindrome as canonical
from solution import even_odd_palindrome as candidate

n = int(sys.argv[1])
print(",".join(map(str, canonical(n))))
print(",".join(map(str, candidate(n))))
PY
  )
  canonical_value=$(sed -n '1p' <<<"$python_values")
  candidate_value=$(sed -n '2p' <<<"$python_values")

  krun_output=$(
    krun submitted-solution.mpy "-cN=$n" \
      --definition audit-semantic-kompiled --output pretty
  )
  k_value=$(
    sed -n \
      's/.*VTuple ( VInt ( \([-0-9]*\) ) , VInt ( \([-0-9]*\) ) ).*/\1,\2/p' \
      <<<"$krun_output"
  )

  printf 'n=%d canonical=%s candidate_python=%s k=%s\n' \
    "$n" "$canonical_value" "$candidate_value" "$k_value"
  test -n "$k_value"
  test "$canonical_value" = "$candidate_value"
  test "$canonical_value" = "$k_value"
done
