#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local rc=$?
  printf '[exit %d]\n' "$rc"
  return 0
}

work=/tmp/audit-work/123-get-odd-collatz/candidate-src

printf 'Stage 2 program-fidelity checks\n'

printf '\nTrusted translator regeneration\n'
printf '$ cd %q && python3 %q %q > %q\n' \
  "$work" \
  /tmp/audit-work/123-get-odd-collatz/trusted/py2mpy.py \
  solution.py solution.regenerated.mpy
(
  cd "$work" || exit 125
  python3 /tmp/audit-work/123-get-odd-collatz/trusted/py2mpy.py \
    solution.py > solution.regenerated.mpy
)
regen_rc=$?
printf '[exit %d]\n' "$regen_rc"
run sha256sum "$work/solution.mpy" "$work/solution.regenerated.mpy"
run cmp -s "$work/solution.mpy" "$work/solution.regenerated.mpy"

printf '\nIndependent canonical-versus-generated differential\n'
run python3 /audit-output/evidence/differential_test.py
