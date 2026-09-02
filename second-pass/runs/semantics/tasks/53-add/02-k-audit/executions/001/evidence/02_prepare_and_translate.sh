#!/usr/bin/env bash
set -u

LOG=/audit-output/evidence/02_prepare_and_translate.log
WORK=/tmp/audit-work/53-add
exec >"$LOG" 2>&1

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local rc=$?
  printf '[exit %d]\n' "$rc"
  return "$rc"
}

run mkdir -p "$WORK" "$WORK/trusted"
run cp -a \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/spec.k \
  /candidate/verification.k \
  /candidate/concrete-tests.mpy \
  /candidate/prove.sh \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  "$WORK/"
run cp -a /candidate/reference-semantics "$WORK/"
run cp -a \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  "$WORK/trusted/"

printf '\n$ cd %q\n' "$WORK"
cd "$WORK" || exit 1
printf '[exit 0]\n'

printf '\n$ python3 trusted/py2mpy.py solution.py > regenerated-solution.mpy\n'
python3 trusted/py2mpy.py solution.py > regenerated-solution.mpy
rc=$?
printf '[exit %d]\n' "$rc"

run cmp -s regenerated-solution.mpy solution.mpy
run sha256sum regenerated-solution.mpy solution.mpy
run diff -u solution.mpy regenerated-solution.mpy
run find . -maxdepth 3 -printf '%y %p -> %l\n'
