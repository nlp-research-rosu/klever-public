#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local rc=$?
  printf '[exit %d]\n' "$rc"
  return "$rc"
}

cd /tmp/audit-work/case || exit 125

printf 'Regenerate submitted MPY with the copied trusted translator:\n'
run python3 /tmp/audit-work/trusted/py2mpy.py solution.py
translate_rc=$?
printf 'The previous command writes its MPY representation to stdout; byte check uses a dedicated output file below.\n'

python3 /tmp/audit-work/trusted/py2mpy.py solution.py > regenerated-solution.mpy
regen_rc=$?
printf '$ python3 /tmp/audit-work/trusted/py2mpy.py solution.py > regenerated-solution.mpy\n'
printf '[exit %d]\n' "$regen_rc"
run cmp -s regenerated-solution.mpy solution.mpy
cmp_rc=$?
run sha256sum regenerated-solution.mpy solution.mpy

printf 'Differential test:\n'
run python3 /audit-output/evidence/02_differential.py
diff_rc=$?

if test "$translate_rc" -ne 0 || test "$regen_rc" -ne 0 || test "$cmp_rc" -ne 0 || test "$diff_rc" -ne 0; then
  exit 1
fi
