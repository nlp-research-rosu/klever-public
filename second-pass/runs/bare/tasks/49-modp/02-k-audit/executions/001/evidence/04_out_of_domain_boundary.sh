#!/usr/bin/env bash
set -u

printf '$ krun /tmp/audit-work/fresh/solution.mpy --definition /tmp/audit-work/fresh/concrete-kompiled -cN=2 -cP=-5\n'
krun /tmp/audit-work/fresh/solution.mpy \
  --definition /tmp/audit-work/fresh/concrete-kompiled \
  -cN=2 \
  -cP=-5
printf '[exit %d]\n' "$?"

printf '\n$ python3 -c %q\n' 'from solution import modp; print(modp(2, -5))'
(
  cd /tmp/audit-work/fresh || exit 1
  python3 -c 'from solution import modp; print(modp(2, -5))'
)
printf '[exit %d]\n' "$?"

printf '\nNOTE: p=-5 does not satisfy the target claim precondition P >Int 0.\n'
