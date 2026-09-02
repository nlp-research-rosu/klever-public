#!/usr/bin/env bash
set +e

WORK=/tmp/audit-work/57-monotonic

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

run mkdir -p "$WORK"
run cp /candidate/solution.py "$WORK/solution.py"
run cp /candidate/solution.mpy "$WORK/submitted-solution.mpy"
run cp /candidate/spec.k "$WORK/spec.k"
run cp /candidate/verification.k "$WORK/verification.k"
run cp /candidate/prove.sh "$WORK/prove.sh"
run cp /reference/py2mpy.py "$WORK/py2mpy.py"
run cp /reference/canonical.py "$WORK/canonical.py"
run cp -a /reference/reference-semantics "$WORK/reference-semantics"

printf '\n$ python3 %q %q > %q\n' \
  "$WORK/py2mpy.py" "$WORK/solution.py" "$WORK/regenerated-solution.mpy"
python3 "$WORK/py2mpy.py" "$WORK/solution.py" > "$WORK/regenerated-solution.mpy"
status=$?
printf '[exit %d]\n' "$status"

run cmp --silent "$WORK/submitted-solution.mpy" "$WORK/regenerated-solution.mpy"
run sha256sum "$WORK/submitted-solution.mpy" "$WORK/regenerated-solution.mpy"
run diff -u "$WORK/submitted-solution.mpy" "$WORK/regenerated-solution.mpy"

# K commands below use solution.mpy, populated only from the trusted translation.
run cp "$WORK/regenerated-solution.mpy" "$WORK/solution.mpy"
