#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/76-is-simple-power
status=0

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  if [ "$rc" -ne 0 ]; then
    status=1
  fi
}

printf '## Trusted contract and implementations\n'
for source in \
  "$scratch/prompt.py" \
  "$scratch/trusted/canonical.py" \
  "$scratch/solution.py" \
  "$scratch/solution.mpy"
do
  printf 'FILE %s\n' "$source"
  nl -ba "$source"
done

printf '\n## Trusted translation regeneration\n'
printf '$ python3 py2mpy.py solution.py > solution-regenerated.mpy\n'
(
  cd "$scratch" &&
    python3 py2mpy.py solution.py > solution-regenerated.mpy
)
translate_rc=$?
printf '[exit %d]\n' "$translate_rc"
if [ "$translate_rc" -ne 0 ]; then
  status=1
fi
run sha256sum "$scratch/solution.mpy" "$scratch/solution-regenerated.mpy"
run cmp -s "$scratch/solution.mpy" "$scratch/solution-regenerated.mpy"

printf '\n## Independent differential execution\n'
run python3 /audit-output/evidence/independent_differential.py

printf '\nSTAGE2_STATUS=%d\n' "$status"
exit "$status"
