#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local command_status=$?
  printf '[exit %d]\n' "$command_status"
  return 0
}

cd /tmp/audit-work/132-is-nested/source || exit 99

printf '$ python3 py2mpy.py concrete_tests.py > regenerated-concrete-tests.mpy\n'
python3 py2mpy.py concrete_tests.py > regenerated-concrete-tests.mpy
translation_status=$?
printf '[exit %d]\n' "$translation_status"
run cmp -s regenerated-concrete-tests.mpy concrete_tests.mpy
run timeout 300s krun regenerated-concrete-tests.mpy \
  --definition runtime-kompiled \
  --output pretty
