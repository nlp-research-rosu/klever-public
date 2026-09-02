#!/usr/bin/env bash
set -uo pipefail

status=0
scratch=/tmp/audit-work/reconstruct-001

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  if (( rc != 0 )); then
    status=1
  fi
}

printf 'Trusted prompt and canonical\n'
nl -ba /reference/prompt.py
nl -ba /reference/canonical.py

printf '\nCandidate implementation\n'
nl -ba "$scratch/solution.py"

printf '\nTrusted translator regeneration\n'
printf '$ cd %q && python3 py2mpy.py solution.py > solution.regenerated.mpy\n' \
  "$scratch"
(
  cd "$scratch"
  python3 py2mpy.py solution.py > solution.regenerated.mpy
)
rc=$?
printf '[exit %d]\n' "$rc"
if (( rc != 0 )); then
  status=1
fi
run cmp "$scratch/solution.regenerated.mpy" "$scratch/solution.mpy"
sha256sum "$scratch/solution.regenerated.mpy" "$scratch/solution.mpy"

printf '\nIndependent canonical differential\n'
run python3 /audit-output/evidence/differential_test.py
sha256sum /audit-output/evidence/differential_cases.json

printf '\nOverall program-fidelity script status=%d\n' "$status"
exit "$status"
